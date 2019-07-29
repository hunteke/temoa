import pyomo.environ
from pyomo.opt import SolverFactory
from pyomo.core import DataPortal
from pyomo.pysp.ef_writer_script_old import *
from IPython import embed as II

def organize_csv():
    from csv import reader, writer
    from collections import OrderedDict
    rows = list()
    tech = list()
    node = list()
    empty_row = ['']*7
    with open('V_ActivityByPeriodAndTech.csv', 'rb') as f:
        csv_reader = reader(f, dialect='excel')
        for row in csv_reader:
            rows.append(row + [''])

    organized_rows = OrderedDict()
    for row in rows:
        this_tech = row[4]
        if row[1] not in node:
            node.append(row[1])
        if this_tech not in tech:
            tech.append(this_tech)
            organized_rows[this_tech] = [row]
        else:
            organized_rows[this_tech].append(row)

    for this_tech in tech:
        for i in range(0, len(organized_rows[this_tech])):
            if organized_rows[this_tech][i][1] != node[i]:
                organized_rows[this_tech].insert(i, empty_row)

    # tech.sort()
    with open('V_ActivityByPeriodAndTech_org.csv', 'wb') as f:
        csv_writer = writer(f, dialect='excel')
        for this_tech in organized_rows:
            row = list()
            for i in organized_rows[this_tech]:
                row += i
            csv_writer.writerow(row)
            

def my_ef_writer(scenario_tree):
    from csv import writer 
    from collections import OrderedDict
    rows = dict() # Key is the variable's name
    for stage in scenario_tree._stages:
        stage_name = stage._name
        for tree_node in stage._tree_nodes:
            tree_node_name = tree_node._name
            for var_id in sorted(tree_node._variable_ids):
                var_name, index = tree_node._variable_ids[var_id]
                row = [str(stage_name), str(tree_node_name), str(var_name)]
                if isinstance(index, str):
                    row += [index]
                else:
                    for i in index:
                        row += [str(i)]
                row += [str(tree_node._solution[var_id])]
                if var_name not in rows:
                    rows[var_name] = [row]
                else:
                    rows[var_name].append(row)

            stage_cost_vardata = tree_node._cost_variable_datas[0][0]
            obj = str(stage_cost_vardata.parent_component().name)
            row = [str(stage_name), str(tree_node_name), str(obj), str(stage_cost_vardata.index()), str(stage_cost_vardata())]
            if obj not in rows:
                rows[obj] = [row]
            else:
                rows[obj].append(row)

    for ofile in rows.keys():
        with open(ofile + '.csv', 'wb') as f:
           csv_writer = writer(f, dialect = 'excel')
           csv_writer.writerows(rows[ofile])
    
    # To calculate V_Activity[p,t]
    if 'V_ActivityByPeriodAndProcess' in rows:
        V_Activity_ptv = rows['V_ActivityByPeriodAndProcess']
        V_Activity_pt  = OrderedDict()
        for row in V_Activity_ptv:
            key = (row[0], row[1], row[2], row[3], row[4]) # (Stage, Node, var_name, p, t)
            if key not in V_Activity_pt:
                V_Activity_pt[key] = float(row[6])
            else:
                V_Activity_pt[key] += float(row[6])

        with open('V_ActivityByPeriodAndTech.csv', 'wb') as f:
            csv_writer = writer(f, dialect = 'excel')
            for key in V_Activity_pt.keys():
                row = list(key) + [V_Activity_pt[key]]
                csv_writer.writerow(row)

def solve_ef(ef_options):
    import os, sys
    sif = ScenarioTreeInstanceFactory(ef_options.model_directory, ef_options.instance_directory, ef_options.verbose)
    scenario_tree = GenerateScenarioTreeForEF(ef_options, sif)
    ef = EFAlgorithmBuilder(ef_options, scenario_tree)
    f = open(os.devnull, 'w'); sys.stdout = f
    ef.solve()
    # ef.save_solution() # This line saves the results into two csv files
    sys.stdout = sys.__stdout__; f.close(); sys.stderr.write('\nrunef output suppressed\n') 
    my_ef_writer(ef._scenario_tree)
    root_node = ef._scenario_tree._stages[0]._tree_nodes[0]
    return root_node.computeExpectedNodeCost()

def solve_pf(p_model, p_data):
    """
    solve_pf(p_model, p_data) -> dict()

    Solves the model in perfect sight mode. 
    p_model -> string, the path to the model file. 
    p_data -> string, the path to the directory of data for the stochastic
    mdoel, where ScenarioStructure.dat should resides.

    Returns a dictionary including the value of objective function for each
    scenario and its conditional probability.
    """

    def return_obj(instance):
        from pyomo.core import Objective
        obj = instance.component_objects(Objective, active = True)
        obj_values = list()
        for o in obj:
            # See section 18.6.3 in Pyomo online doc
            # https://taizilongxu.gitbooks.io/stackoverflow-about-python/content/59/README.html
            method_obj = getattr(instance, str(o))
            obj_values.append(method_obj())
        # Assuming there is only one objective function
        return obj_values[0]

        # Out-of-date for Pyomo 4.1
        # obj = instance.active_components(Objective) 
        # objs = obj.items()[0]
        # obj_name, obj_value = objs[0], value(objs[1]())
        # return obj_value

    import sys, os
    from collections import deque, defaultdict
    from pyomo.pysp.util.scenariomodels import scenario_tree_model
    from pyomo.core import Objective

    (head, tail) = os.path.split(p_model)
    sys.path.insert(0, head)
    pwd = os.getcwd()
    os.chdir(p_data)

    s2fp_dict = defaultdict(deque) # Scenario to 'file path' dictionary, .dat not included
    s2cd_dict = defaultdict(float) # Scenario to conditonal density mapping
    sStructure = scenario_tree_model.create_instance( filename='ScenarioStructure.dat' )

    # The following code is borrowed from Kevin's temoa_lib.py
    ###########################################################################
    # Step 1: find the root node.  PySP doesn't make this very easy ...
    
    # a child -> parent mapping, because every child has only one parent, but
    # not vice-versa
    ctpTree = dict() # Child to parent dict, one to one mapping
    
    to_process = deque()
    to_process.extend( sStructure.Children.keys() )
    while to_process:
            node = to_process.pop()
            if node in sStructure.Children:
                    # it's a parent!
                    new_nodes = set( sStructure.Children[ node ] )
                    to_process.extend( new_nodes )
                    ctpTree.update({n : node for n in new_nodes })
    
                     # parents           -     children
    root_node = (set( ctpTree.values() ) - set( ctpTree.keys() )).pop()
    
    # ptcTree = defaultdict( list ) # Parent to child node, one to multiple mapping
    # for c, p in ctpTree.items():
    #         ptcTree[ p ].append( c )
    # ptcTree = dict( ptcTree )   # be slightly defensive; catch any additions
    
    # leaf_nodes = set(ctpTree.keys()) - set(ctpTree.values())
    leaf_nodes = set(sStructure.ScenarioLeafNode.values()) # Try to hack Kevin's code
    
    scenario_nodes = dict() # Map from leafnode to 'node path'
    for node in leaf_nodes: # e.g.: {Rs0s0: [R, Rs0, Rs0s0]}
            s = deque()
            scenario_nodes[ node ] = s
            while node in ctpTree:
                    s.append( node )
                    node = ctpTree[ node ]
            s.append( node )
            s.reverse()
    ###########################################################################

    for s in sStructure.Scenarios:
        cp = 1.0 # Starting probability
        for n in scenario_nodes[sStructure.ScenarioLeafNode[s]]:
            cp = cp*sStructure.ConditionalProbability[n]
            if not sStructure.ScenarioBasedData.value:
                s2fp_dict[s].append(n + '.dat')
        s2cd_dict[s] = cp
    
    from pyomo.core import Objective
    if sStructure.ScenarioBasedData.value:
        for s in sStructure.Scenarios:
            s2fp_dict[s].append(s + '.dat')

    model_module = __import__(tail[:-3], globals(), locals())
    model = model_module.model
    pf_result = {'cost': list(), 'cd': list()}
    for s in sStructure.Scenarios:
        pf_result['cd'].append(s2cd_dict[s])
        data = DataPortal(model=model)
        for dat in s2fp_dict[s]:
            data.load(filename=dat)
        instance = model.create_instance(data)
        optimizer = SolverFactory('cplex')
        results = optimizer.solve(instance)

        instance.solutions.load_from(results)
        # instance.load(results)
        obj_val = return_obj(instance)
        pf_result['cost'].append(obj_val)
        sys.stdout.write('\nSolved .dat(s) {}\n'.format(s2fp_dict[s]))
        sys.stdout.write('    Total cost: {}\n'.format(obj_val))
		# instance.load does not work for Pyomo 4.1
        # if instance.load(results): 
        #     obj_val = return_obj(instance)
        #     pf_result['cost'].append(obj_val)
        #     sys.stdout.write('\nSolved .dat(s) {}\n'.format(s2fp_dict[s]))
        #     sys.stdout.write('    Total cost: {}\n'.format(obj_val))
        # else:
        #     pf_result['cost'].append(None)
        #     sys.stdout.write('\nSolved .dat(s) {}\n'.format(s2fp_dict[s]))
        #     sys.stdout.write('    This scenario has no feasible solution.\n')
    os.chdir(pwd)
    return pf_result

def compute_evpi(ef_result, pf_result):
    pf = 0
    for i in range(0, len(pf_result['cost'])):
        pf += pf_result['cd'][i]*pf_result['cost'][i]
    return ef_result - pf

def test_sudan():
    from time import time
    import sys
    sys.stderr.write('\nSolving Sudan problem\n')
    sys.stderr.write('-'*25 + '\n')
    p_model = '/afs/unity.ncsu.edu/users/n/nspatank/temoa/temoa_stoch_original_cap_cost/temoa_model/temoa_stochastic.py'
    p_data  = '/afs/unity.ncsu.edu/users/n/nspatank/temoa/temoa_stoch_original_cap_cost/stochastic/S_Sudan_small'
    sys.stderr.write('\nSolving perfect sight mode\n')
    pf_result = solve_pf(p_model, p_data)
    ef_args = ['-m', p_model, '-i', p_data, '--solver', 'cplex', '--solve', '--solution-writer', 'pyomo.pysp.plugins.csvsolutionwriter']
    ef_option_parser = construct_ef_writer_options_parser('runef [options]')
    start_time = time()
    (ef_options, args) = ef_option_parser.parse_args(args=ef_args)
    sys.stderr.write('\nSolving extensive form\n')
    ef_result = solve_ef(ef_options)
    msg = '\nrunef time: {} s\n'.format(time() - start_time)
    msg += 'runef objective value: {}\n'.format(ef_result)
    msg += 'EVPI: {}\n'.format(compute_evpi(ef_result, pf_result))
    sys.stderr.write(msg)

def test_sudan_VSS():
    from time import time
    import sys
    sys.stderr.write('\nSolving Sudan problem\n')
    sys.stderr.write('-'*25 + '\n')
    p_model = '/home/arqueiroz/SSudan/S1_2_H/temoa_model/temoa_stochastic.py'
    p_data  = '/home/arqueiroz/SSudan/S1_2_H/stochastic/S_Sudan_original_stoch_cap_cost_11'
    sys.stderr.write('\nSolving perfect sight mode\n')
    pf_result = solve_pf(p_model, p_data)
    ef_args = ['-m', p_model, '-i', p_data, '--solver', 'cplex', '--solve', '--solution-writer', 'pyomo.pysp.plugins.csvsolutionwriter']
    ef_option_parser = construct_ef_writer_options_parser('runef [options]')
    start_time = time()
    (ef_options, args) = ef_option_parser.parse_args(args=ef_args)
    sys.stderr.write('\nSolving extensive form\n')
    ef_result = solve_ef(ef_options)
    msg = '\nrunef time: {} s\n'.format(time() - start_time)
    msg += 'runef objective value: {}\n'.format(ef_result)
    msg += 'EVPI: {}\n'.format(compute_evpi(ef_result, pf_result))
    sys.stderr.write(msg)
    return compute_evpi(ef_result, pf_result) # Adding to return a value

def test_two_tech():
    from time import time
    import sys
    sys.stderr.write('\nSolving temoa problem: two tech\n')
    sys.stderr.write('-'*25 + '\n')
    p_model = 'D:\\temoa\\temoa\\temoa_model\\temoa_stochastic.py'
    p_data  = 'D:\\temoa\\temoa\\stochastic\\test_twotechs_1'
    sys.stderr.write('\nSolving perfect sight mode\n')
    pf_result = solve_pf(p_model, p_data)
    ef_args = ['-m', p_model, '-i', p_data, '--solver', 'cplex', '--solve', '--solution-writer', 'pyomo.pysp.plugins.csvsolutionwriter']
    ef_option_parser = construct_ef_writer_options_parser('runef [options]')
    start_time = time()
    (ef_options, args) = ef_option_parser.parse_args(args=ef_args)
    sys.stderr.write('\nSolving extensive form\n')
    ef_result = solve_ef(ef_options)
    msg = '\nrunef time: {} s\n'.format(time() - start_time)
    msg += 'runef objective value: {}\n'.format(ef_result)
    msg += 'EVPI: {}\n'.format(compute_evpi(ef_result, pf_result))
    sys.stderr.write(msg)

def test_utopia():
    from time import time
    import sys
    sys.stderr.write('\nSolving temoa problem: utopia\n')
    sys.stderr.write('-'*25 + '\n')
    p_model = 'D:/temoa/temoa_stoch_original_cap_cost/temoa_model/temoa_stochastic.py'
    p_data  = 'D:/temoa/temoa_stoch_original_cap_cost/stochastic/utopia_demand'
    sys.stderr.write('\nSolving perfect sight mode\n')
    pf_result = solve_pf(p_model, p_data)
    ef_args = ['-m', p_model, '-i', p_data, '--solver', 'glpk', '--solve']
    ef_option_parser = construct_ef_writer_options_parser('runef [options]')
    start_time = time()
    (ef_options, args) = ef_option_parser.parse_args(args=ef_args)
    sys.stderr.write('\nSolving extensive form\n')
    ef_result = solve_ef(ef_options)
    msg = '\nrunef time: {} s\n'.format(time() - start_time)
    msg += 'runef objective value: {}\n'.format(ef_result)
    msg += 'EVPI: {}\n'.format(compute_evpi(ef_result, pf_result))
    sys.stderr.write(msg)

def test_USND():
    from time import time
    import sys
    sys.stderr.write('\nSolving temoa problem: USND\n')
    sys.stderr.write('-'*25 + '\n')
    p_model = '/home/bli/Temoa_git/temoa/temoa_model/temoa_stochastic.py'
    p_data  = '/home/bli/TEMOA/Stochastic/USND'
    sys.stderr.write('\nSolving perfect sight mode\n')
    pf_result = solve_pf(p_model, p_data)
    ef_args = ['-m', p_model, '-i', p_data, '--solver', 'glpk', '--solve', '--solution-writer', 'pyomo.pysp.plugins.csvsolutionwriter']
    ef_option_parser = construct_ef_writer_options_parser('runef [options]')
    (ef_options, args) = ef_option_parser.parse_args(args=ef_args)
    start_time = time()
    sys.stderr.write('\nSolving extensive form\n')
    ef_result = solve_ef(ef_options)
    msg = '\nrunef time: {} s\n'.format(time() - start_time)
    msg += 'runef objective value: {}\n'.format(ef_result)
    msg += 'EVPI: {}\n'.format(compute_evpi(ef_result, pf_result))
    sys.stderr.write(msg)

if __name__ == '__main__':
    test_sudan_VSS()
    # test_two_tech()
    # test_utopia()
    # test_USND()
