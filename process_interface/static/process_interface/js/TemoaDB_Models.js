;(function () {

"use strict";  // ECMA v5 pragma, similar to Perl's functionality.
  // FYI: http://ejohn.org/blog/ecmascript-5-strict-mode-json-and-more/

if ( !('Temoa' in window) ) {
	var msg = 'Error: The Temoa namespace is not defined.  Cannot continue.';
	msg += '\n\nThis likely means that one or more TemoaUI files did not ';
	msg += 'download from the server, implying at least a transient network ';
	msg += 'failure.  In most cases, <strong>a simple reload of this page will ';
	msg += 'fix the issue</strong>.  If not, however, please share the problem ';
	msg += '-- and importantly, how to create it -- on the Temoa Project forum.';
	console.error( msg )
	throw msg;
}

///////////////////////////////////////////////////////////////////////////////
//                                  Analysis                                 //
///////////////////////////////////////////////////////////////////////////////

Temoa.canModel.Commodity = can.Model('Commodity', {
	findOne: 'GET ' + Temoa.C.ROOT_URL + '/analysis/{aId}/commodity/{id}',
	attributes: {
		aId: 'int',
		id:  'int',
		name: 'string',
	}
}, {});

Temoa.canModel.CommodityDemand = Temoa.canModel.Commodity.extend('CommodityDemand', {
	destroy: function ( id ) {
		var url = Temoa.C.ROOT_URL;
		url += '/analysis/{aId}/delete/commodity/{id}';
		url = Temoa.fn.replaceNamedArgs( url, this.store[ id ].attr() );
		return $.ajax({ type: 'DELETE', url: url });
	},
	create:  'POST ' + Temoa.C.ROOT_URL + '/analysis/{aId}/create/commodity/demand',
	update:  'POST ' + Temoa.C.ROOT_URL + '/analysis/{aId}/update/commodity/{id}',
}, {
});
Temoa.canModel.CommodityEmission = Temoa.canModel.Commodity.extend('CommodityEmission', {
	destroy: function ( id ) {
		var url = Temoa.C.ROOT_URL;
		url += '/analysis/{aId}/delete/commodity/{id}';
		url = Temoa.fn.replaceNamedArgs( url, this.store[ id ].attr() );
		return $.ajax({ type: 'DELETE', url: url });
	},
	create:  'POST ' + Temoa.C.ROOT_URL + '/analysis/{aId}/create/commodity/emission',
	update:  'POST ' + Temoa.C.ROOT_URL + '/analysis/{aId}/update/commodity/{id}',
}, {});
Temoa.canModel.CommodityPhysical = Temoa.canModel.Commodity.extend('CommodityPhysical', {
	destroy: function ( id ) {
		var url = Temoa.C.ROOT_URL;
		url += '/analysis/{aId}/delete/commodity/{id}';
		url = Temoa.fn.replaceNamedArgs( url, this.store[ id ].attr() );
		return $.ajax({ type: 'DELETE', url: url });
	},
	create:  'POST ' + Temoa.C.ROOT_URL + '/analysis/{aId}/create/commodity/physical',
	update:  'POST ' + Temoa.C.ROOT_URL + '/analysis/{aId}/update/commodity/{id}',
}, {});

Temoa.canModel.Commodities = can.Model('Commodities', {
	findAll: 'GET ' + Temoa.C.ROOT_URL + '/analysis/{aId}/commodity/list',
	attributes: {
		demand:   'CommodityDemand.models',
		emission: 'CommodityEmission.models',
		physical: 'CommodityPhysical.models',
	}
}, {});

Temoa.canModel.SegFrac = can.Model('SegFrac', {
	create:  'POST '   + Temoa.C.ROOT_URL + '/analysis/{aId}/segfrac/create',
	update:  'POST '   + Temoa.C.ROOT_URL + '/analysis/{aId}/segfrac/update/{id}',
	destroy: 'DELETE ' + Temoa.C.ROOT_URL + '/analysis/{aId}/segfrac/remove/{id}',
	attributes: {
		aId: 'int',
		id: 'int',
		season: 'string',
		time_of_day: 'string',
		value: 'number'
	}
}, {
	name: can.compute( function ( ) {
		var s = this.attr('season'), tod = this.attr('time_of_day');
		if ( s && tod )
			return s + ', ' + tod;
		return '';
	}),
	partialUpdate: function ( id, attr ) {
		var url = Temoa.C.ROOT_URL;
		url += '/analysis/{aId}/segfrac/update/{id}';
		url = Temoa.fn.replaceNamedArgs( url, this.attr() );
		return $.post( url, attr );
	}
});

Temoa.canModel.DemandDefaultDistribution = can.Model('DemandDefaultDistribution', {
	create:  'POST '   + Temoa.C.ROOT_URL + '/analysis/{aId}/demanddefaultdistribution/create/segfrac/{sfId}',
	update:  'POST '   + Temoa.C.ROOT_URL + '/analysis/{aId}/demanddefaultdistribution/update/{id}',
	destroy: 'DELETE ' + Temoa.C.ROOT_URL + '/analysis/{aId}/demanddefaultdistribution/remove/{id}',
	attributes: {
		aId: 'int',
		sfId: 'int',
		id: 'int',
		timeslice: 'SegFrac.model',
		value: 'number'
	}
}, {
	partialUpdate: function ( id, attr ) {
		var url = Temoa.C.ROOT_URL;
		url += '/analysis/{aId}/demanddefaultdistribution/update/{id}';
		url = replaceNamedArgs( url, this.attr() );
		return $.post( url, attr );
	}
});

Temoa.canModel.DemandSpecificDistribution = can.Model('DemandSpecificDistribution', {
	create:  'POST '   + Temoa.C.ROOT_URL + '/analysis/{aId}/demandspecificdistribution/create/segfrac/{sfId}/demand/{dId}',
	update:  'POST '   + Temoa.C.ROOT_URL + '/analysis/{aId}/demandspecificdistribution/update/{id}',
	destroy: 'DELETE ' + Temoa.C.ROOT_URL + '/analysis/{aId}/demandspecificdistribution/remove/{id}',
	attributes: {
		aId: 'int',
		dId: 'int',
		sfId: 'int',
		id: 'int',
		timeslice: 'SegFrac.model',
		value: 'number'
	}
}, {
	partialUpdate: function ( id, attr ) {
		var url = Temoa.C.ROOT_URL;
		url += '/analysis/{aId}/demandspecificdistribution/update/{id}';
		url = Temoa.fn.replaceNamedArgs( url, this.attr() );
		return $.post( url, attr );
	}
});

Temoa.canModel.Demand = can.Model('Demand', {
	create:  'POST '   + Temoa.C.ROOT_URL + '/analysis/{aId}/demand/create/commodity/{cId}/period/{period}',
	update:  'POST '   + Temoa.C.ROOT_URL + '/analysis/{aId}/demand/update/{id}',
	destroy: 'DELETE ' + Temoa.C.ROOT_URL + '/analysis/{aId}/demand/remove/{id}',
	attributes: {
		aId: 'int',
		cId: 'int',
		id: 'int',
		commodity_name: 'string',
		period: 'int',
		value: 'number'
	}
}, {
	name: can.compute( function ( ) {
		var d = this.attr('commodity_name'), p = this.attr('period');
		if ( d && p )
			return d + ', ' + p;
		return '';
	}),
	partialUpdate: function ( id, attr ) {
		var url = Temoa.C.ROOT_URL;
		url += '/analysis/{aId}/demand/update/{id}';
		url = Temoa.fn.replaceNamedArgs( url, this.attr() );
		return $.post( url, attr );
	}
});

Temoa.canModel.Analysis = can.Model('Analysis', {
	findAll: 'GET ' + Temoa.C.ROOT_URL + '/analysis/list',
	findOne: 'GET ' + Temoa.C.ROOT_URL + '/analysis/view/{aId}',
	create:  function ( attrs ) {
		var url = Temoa.C.ROOT_URL;
		url += '/analysis/create';
		return $.post( url, attrs, 'json' );
	},
	update:  function ( id, attrs ) {
		var url = Temoa.C.ROOT_URL;
		url += '/analysis/{aId}/update';
		url = url.replace( /{aId}/, attrs.id );
		return $.post( url, attrs, 'json' );
	},
	destroy: 'DELETE ' + Temoa.C.ROOT_URL + '/analysis/remove/{aId}',
	attributes: {
		id: 'int',
		username: 'string',
		name: 'string',
		description: 'string',
		global_discount_rate: 'number',
		vintages: 'string',
		period_0: 'int',
		segfracs: 'SegFrac.models',

		// Comments left to show intended connection.  Problem: CanJS can't
		// return a /dictionary/ of Models, so instead dynamically create as a
		// Map of Maps, and convert each item to models during initialization.
		// (For implementation, search for 'ddd' below.)
//		demanddefaultdistribution: 'DemandDefaultDistribution.models',
//		demandspecificdistribution: 'DemandSpecificDistribution.models',
//		future_demands: 'Demand.models',
		commodity_demand:   'CommodityDemand.models',
		commodity_emission: 'CommodityEmission.models',
		commodity_physical: 'CommodityPhysical.models',
	}
}, {
	partialUpdate: function ( id, attr ) {
		var url = Temoa.C.ROOT_URL;
		url += '/analysis/{aId}/update';
		url = Temoa.fn.replaceNamedArgs( url, this.attr() );
		return $.post( url, attr );
	},
	download_name: function ( ) {
		var name = this.name;
		name = name.replace( / +/g, '_' );
		name = name.replace( /\W/g, '' );
		name = name.replace( /(\.[Dd][Aa][Tt])+$/, '' );
		name = name + '.dat';
		return name;
	},
	download_url: function ( ) {
		var url = Temoa.C.ROOT_URL;
		url += '/analysis/{id}/download_as_dat';
		url = Temoa.fn.replaceNamedArgs( url, this.attr() );
		return url;
	},
	segFracSum: can.compute( function ( style ) {
		var sum = 0, epsilon = 1e-6;
		this.segfracs.each( function ( sf ) {
			sum += sf.attr('value') || 0;
		});
		sum = Number(sum.toFixed( 6 ));

		if ( 'html' === style ) {
			if ( Math.abs(1 - sum) > epsilon )
				return "<span class='error'>" + sum + '</span>';
			else
				return sum
		}

		return sum;
	}),
	dddFracSum: can.compute( function ( style ) {
		var sum = 0, ddd_list = this.demanddefaultdistribution, epsilon = 1e-6;
		this.segfracs.each( function ( sf ) {
			sum += ddd_list[ sf.name() ].attr('value') || 0;
		});
		sum = Number(sum.toFixed( 6 ));

		if ( 'html' === style ) {
			if ( Math.abs(1 - sum) > epsilon )
				return "<span class='error'>" + sum + '</span>';
			else
				return sum;
		}

		return sum;
	}),
});

///////////////////////////////////////////////////////////////////////////////
//                                 Technology                                //
///////////////////////////////////////////////////////////////////////////////

Temoa.canModel.Technology = can.Model('Technology', {
	findAll: 'GET '  + Temoa.C.ROOT_URL + '/analysis/{aId}/technology/list',
	findOne: 'GET '  + Temoa.C.ROOT_URL + '/analysis/{aId}/technology/info/{id}',
	update:  'POST ' + Temoa.C.ROOT_URL + '/analysis/{aId}/technology/update/{id}',
	attributes: {
		id:       'int',
		aId:      'int',
		name:     'string',
		description: 'string',
		baseload: 'boolean',
		storage:  'boolean',
		lifetime: 'number',
		loanlife: 'number',
		capacitytoactivity: 'number',
		growthratelimit: 'number',
		growthrateseed: 'number',
		capacityfactors: 'TechnologyCapacityFactor.models',
		inputsplits: 'TechnologyInputSplit.models',
		outputsplits: 'TechnologyOutputSplit.models',
	}
}, {
	partialUpdate: function ( id, attr ) {
		var url = Temoa.C.ROOT_URL;
		url += '/analysis/{aId}/technology/update/{id}';
		url = Temoa.fn.replaceNamedArgs( url, this.attr() );
		return $.post( url, attr );
	}
});

Temoa.canModel.TechnologyCapacityFactor = can.Model('TechnologyCapacityFactor', {
	create:  'POST ' + Temoa.C.ROOT_URL + '/analysis/{aId}/technology/{tId}/CapacityFactor/create',
	update:  'POST ' + Temoa.C.ROOT_URL + '/analysis/{aId}/technology/{tId}/CapacityFactor/update/{id}',
	destroy: function ( id ) {
		var url = Temoa.C.ROOT_URL;
		url += '/analysis/{aId}/technology/{tId}/CapacityFactor/remove/{id}';
		url = Temoa.fn.replaceNamedArgs( url, this.store[ id ].attr() );
		return $.ajax({ type: 'DELETE', url: url });
	},
	attributes: {
		aId:     'int',
		tId:     'int',
		id:      'int',
		sfId:    'int',
		segfrac: 'SegFrac.model',
		value:   'number',
	}
}, {
	partialUpdate: function ( id, attr ) {
		var url = Temoa.C.ROOT_URL;
		url += '/analysis/{aId}/technology/{tId}/CapacityFactor/update/{id}';
		url = Temoa.fn.replaceNamedArgs( url, this.attr() );
		return $.post( url, attr );
	}
});

Temoa.canModel.TechnologyInputSplit = can.Model('TechnologyInputSplit', {
	create:  'POST ' + Temoa.C.ROOT_URL + '/analysis/{aId}/technology/{tId}/InputSplit/create',
	update:  'POST ' + Temoa.C.ROOT_URL + '/analysis/{aId}/technology/{tId}/InputSplit/update/{id}',
	destroy: function ( id ) {
		var url = Temoa.C.ROOT_URL;
		url += '/analysis/{aId}/technology/{tId}/InputSplit/remove/{id}';
		url = Temoa.fn.replaceNamedArgs( url, this.store[ id ].attr() );
		return $.ajax({ type: 'DELETE', url: url });
	},
	attributes: {
		'aId'   : 'int',
		'tId'   : 'int',
		'id'    : 'int',
		'inp'   : 'string',
		'value' : 'number',
	}
}, {
	partialUpdate: function ( id, attr ) {
		var url = Temoa.C.ROOT_URL;
		url += '/analysis/{aId}/technology/{tId}/InputSplit/update/{id}';
		url = Temoa.fn.replaceNamedArgs( url, this.attr() );
		return $.post( url, attr );
	}
});

Temoa.canModel.TechnologyOutputSplit = can.Model('TechnologyOutputSplit', {
	findAll: 'GET ' + Temoa.C.ROOT_URL + '/analysis/{aId}/technology/{tId}/OutputSplit/list',
	findOne: 'GET ' + Temoa.C.ROOT_URL + '/analysis/{aId}/technology/{tId}/OutputSplit/{id}',
	create:  'POST ' + Temoa.C.ROOT_URL + '/analysis/{aId}/technology/{tId}/OutputSplit/create',
	update:  'POST ' + Temoa.C.ROOT_URL + '/analysis/{aId}/technology/{tId}/OutputSplit/update/{id}',
	destroy: function ( id ) {
		var url = Temoa.C.ROOT_URL;
		url += '/analysis/{aId}/technology/{tId}/OutputSplit/remove/{id}';
		url = Temoa.fn.replaceNamedArgs( url, this.store[ id ].attr() );
		return $.ajax({ type: 'DELETE', url: url });
	},
	attributes: {
		'aId'   : 'int',
		'tId'   : 'int',
		'id'    : 'int',
		'out'   : 'string',
		'value' : 'number',
	}
}, {
	partialUpdate: function ( id, attr ) {
		var url = Temoa.C.ROOT_URL;
		url += '/analysis/{aId}/technology/{tId}/OutputSplit/update/{id}';
		url = Temoa.fn.replaceNamedArgs( url, this.attr() );
		return $.post( url, attr );
	}
});

///////////////////////////////////////////////////////////////////////////////
//                                  Process                                  //
///////////////////////////////////////////////////////////////////////////////

Temoa.canModel.Process = can.Model('Process', {
	findAll: 'GET ' + Temoa.C.ROOT_URL + '/analysis/{aId}/process/list/json',
	findOne: 'GET ' + Temoa.C.ROOT_URL + '/analysis/{aId}/process/info/{id}',
	create:  'POST ' + Temoa.C.ROOT_URL + '/analysis/{aId}/process/create',
	update:  'POST ' + Temoa.C.ROOT_URL + '/analysis/{aId}/process/update/{id}',
	destroy: function ( id ) {
		var url = Temoa.C.ROOT_URL;
		url += '/analysis/{aId}/process/remove/{id}';
		url = Temoa.fn.replaceNamedArgs( url, this.store[ id ].attr() );
		return $.ajax({ type: 'DELETE', url: url });
	},
	attributes: {
		id: 'int',
		aId: 'int',  // for updating, deleting (the urls)
		technology:         'Technology.model',
		capacityfactors:    'ProcessCapacityFactor.models',
		costsfixed:         'ProcessCostFixed.models',
		costsvariable:      'ProcessCostVariable.models',
		efficiencies:       'ProcessEfficiency.models',
		emissionactivities: 'ProcessEmissionActivity.models',
	},
}, {
	partialUpdate: function ( id, attr ) {
		var url = Temoa.C.ROOT_URL;
		url += '/analysis/{aId}/process/update/{id}';
		url = Temoa.fn.replaceNamedArgs( url, this.attr() );
		return $.post( url, attr );
	},
});

Temoa.canModel.ProcessCapacityFactor = can.Model('ProcessCapacityFactor', {
	create:  'POST ' + Temoa.C.ROOT_URL + '/analysis/{aId}/process/{pId}/CapacityFactor/create',
	update:  'POST ' + Temoa.C.ROOT_URL + '/analysis/{aId}/process/{pId}/CapacityFactor/update/{id}',
	destroy: function ( id ) {
		var url = Temoa.C.ROOT_URL;
		url += '/analysis/{aId}/process/{pId}/CapacityFactor/remove/{id}';
		url = Temoa.fn.replaceNamedArgs( url, this.store[ id ].attr() );
		return $.ajax({ type: 'DELETE', url: url });
	},
	attributes: {
		aId:     'int',
		pId:     'int',
		id:      'int',
		sfId:    'int',
		segfrac: 'SegFrac.model',
		value:   'number',
	}
}, {
	partialUpdate: function ( id, attr ) {
		var url = Temoa.C.ROOT_URL;
		url += '/analysis/{aId}/process/{pId}/CapacityFactor/update/{id}';
		url = Temoa.fn.replaceNamedArgs( url, this.attr() );
		return $.post( url, attr );
	}
});

Temoa.canModel.ProcessCostFixed = can.Model('ProcessCostFixed', {
	create:  'POST ' + Temoa.C.ROOT_URL + '/analysis/{aId}/process/{pId}/create/CostFixed',
	update:  'POST ' + Temoa.C.ROOT_URL + '/analysis/{aId}/process/{pId}/update/CostFixed/{id}',
	destroy: function ( id ) {
		var url = Temoa.C.ROOT_URL;
		url += '/analysis/{aId}/process/{pId}/remove/CostFixed/{id}';
		url = Temoa.fn.replaceNamedArgs( url, this.store[ id ].attr() );
		return $.ajax({ type: 'DELETE', url: url });
	},
	attributes: {
		aId:   'int',   // for updating, deleting (the urls)
		pId:   'int',   // for updating, deleting (the urls)
		id:    'int',
		period: 'int',
		value: 'number'
	}
}, {
	partialUpdate: function ( id, attr ) {
		var url = Temoa.C.ROOT_URL;
		url += '/analysis/{aId}/process/{pId}/update/CostFixed/{id}';
		url = Temoa.fn.replaceNamedArgs( url, this.attr() );
		return $.post( url, attr );
	}
});

Temoa.canModel.ProcessCostVariable = can.Model('ProcessCostVariable', {
	create:  'POST ' + Temoa.C.ROOT_URL + '/analysis/{aId}/process/{pId}/create/CostVariable',
	update:  'POST ' + Temoa.C.ROOT_URL + '/analysis/{aId}/process/{pId}/update/CostVariable/{id}',
	destroy: function ( id ) {
		var url = Temoa.C.ROOT_URL;
		url += '/analysis/{aId}/process/{pId}/remove/CostVariable/{id}';
		url = Temoa.fn.replaceNamedArgs( url, this.store[ id ].attr() );
		return $.ajax({ type: 'DELETE', url: url });
	},
	attributes: {
		aId:   'int',   // for updating, deleting (the urls)
		pId:   'int',   // for updating, deleting (the urls)
		id:    'int',
		period: 'int',
		value: 'number'
	}
}, {
	partialUpdate: function ( id, attr ) {
		var url = Temoa.C.ROOT_URL;
		url += '/analysis/{aId}/process/{pId}/update/CostVariable/{id}';
		url = Temoa.fn.replaceNamedArgs( url, this.attr() );
		return $.post( url, attr );
	}
});

Temoa.canModel.ProcessEfficiency = can.Model('ProcessEfficiency', {
	create:  'POST ' + Temoa.C.ROOT_URL + '/analysis/{aId}/process/{pId}/create/Efficiency',
	update:  'POST ' + Temoa.C.ROOT_URL + '/analysis/{aId}/process/{pId}/update/Efficiency/{id}',
	destroy: function ( id ) {
		var url = Temoa.C.ROOT_URL;
		url += '/analysis/{aId}/process/{pId}/remove/Efficiency/{id}';
		url = Temoa.fn.replaceNamedArgs( url, this.store[ id ].attr() );
		return $.ajax({ type: 'DELETE', url: url });
	},
	attributes: {
		aId:   'int',   // for updating, deleting (the urls)
		pId:   'int',   // for updating, deleting (the urls)
		id:    'int',
		inp:   'string',
		out:   'string',
		value: 'number'
	}
}, {
	partialUpdate: function ( id, attr ) {
		var url = Temoa.C.ROOT_URL;
		url += '/analysis/{aId}/process/{pId}/update/Efficiency/{id}';
		url = Temoa.fn.replaceNamedArgs( url, this.attr() );
		return $.post( url, attr );
	}
});

Temoa.canModel.ProcessEmissionActivity = can.Model('ProcessEmissionActivity', {
	create:  'POST ' + Temoa.C.ROOT_URL + '/analysis/{aId}/process/{pId}/create/EmissionActivity',
	update:  'POST ' + Temoa.C.ROOT_URL + '/analysis/{aId}/Efficiency/{eId}/update/EmissionActivity/{id}',
	destroy: function ( id ) {
		var url = Temoa.C.ROOT_URL;
		url += '/analysis/{aId}/Efficiency/{eId}/remove/EmissionActivity/{id}';
		url = Temoa.fn.replaceNamedArgs( url, this.store[ id ].attr() );
		return $.ajax({ type: 'DELETE', url: url });
	},
	attributes: {
		aId: 'int',   // for updating, deleting (the urls)
		pId: 'int',   // for updating, deleting (the urls)
		eId: 'int',   // for attaching existing efficiency after collection
		id: 'int',
		pollutant: 'string',
		efficiency: 'ProcessEfficiency.model',
		value: 'number'
	}
}, {
	partialUpdate: function ( id, attr ) {
		var url = Temoa.C.ROOT_URL;
		url += '/analysis/{aId}/Efficiency/{eId}/update/EmissionActivity/{id}';
		url = Temoa.fn.replaceNamedArgs( url, this.attr() );
		return $.post( url, attr );
	}
});

})();

console.log( 'TemoaDB model definitions loaded: ' + Date() );
