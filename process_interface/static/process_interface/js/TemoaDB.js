(function () {

"use strict";  // ECMA v5 pragma, similar to Perl's functionality.
  // FYI: http://ejohn.org/blog/ecmascript-5-strict-mode-json-and-more/

// The Temoa namespace
//
// Assume the word 'Temoa' is sufficiently unique in development circles: if
// it exists, then assume some other Temoa related library has already loaded
// and use it as our namespace.  Meanwhile, if it doesn't exist, create it.
var Temoa;

if ( 'Temoa' in window ) {
	Temoa = window.Temoa;
} else {
	window.Temoa = Temoa = {
	  C:     {}, // constants
	  vars:  {}, // variables
	  fn:    {}, // functions
	  eventHandler: {},  // also functions; but specifically for handling events
	  canModel:   {},
	  canControl: {},
	};
}

Temoa.C.COOKIE = 'TemoaUISettings';
Temoa.C.DEBUG = window.location.search.indexOf( 'debug=true' ) > -1;
Temoa.C.ROOT_URL = window.location.pathname.replace( '/interact/', '' );

// cachedScript borrowed from the jQuery docs
jQuery.cachedScript = function( url, options ) {
	// Allow user to set any option except for dataType, cache, and url
	options = $.extend( options || {}, {
	  dataType: "script",
	  cache: true,
	  url: url
	});

	// Use $.ajax() since it is more flexible than $.getScript
	// Return the jqXHR object so we can chain callbacks
	return jQuery.ajax( options );
};

var activeAnalysisList   = null
  , activeTechnologyList = null
  , activeProcessList    = null
  ;


can.Control('AnalysisCommodityLists', {
	defaults: {
			view: Temoa.C.ROOT_URL + '/client_template/analysis_commodities.ejs'
		}
	},{
	init: function ( $el, options ) {
		var view = options.view;
		if ( Temoa.C.DEBUG )
			view += '?_=' + new Date().getTime();

		this.analysis = options.analysis;
		var analysis = this.analysis;  // needed for closure, below

		$el.html( can.view( view, {
			analysis: analysis,
			username: Temoa.fn.getCookie().username || null,
		}));

		$('#AnalysisCommoditiesCloseButton').click( function ( ) {
			$('#ShowHideCommodities').click();
		});

		var username = Temoa.fn.getCookie().username;
		if ( ! (username && username === analysis.username ) )
			return;

		function select_start () {
			var $others = $(this).closest( 'form' ).find( 'tbody' ).not( this );
			$others.find('.ui-selected').removeClass( 'ui-selected' );
			$('#commodity_detail').fadeOut();
		}
		function select_stop () {
			var $info = $('#commodity_detail');

			var $sel = $( this ).find( 'tr.ui-selected' );
			var coms = new Array();
			for ( var i = 0; i < $sel.length; ++i ) {
				coms.push( $($sel[i]).data().commodity );
			}
			if ( ! (coms.length > 0) ) {
				return;
			}
			var username = Temoa.fn.getCookie().username || null;

			function createCommodityDetail ( toCreate ) {
				new CommodityDetail( $info, {
					analysis:  analysis,
					commodity: toCreate.shift(),
					username:  username
				});

				if ( toCreate.length > 0 ) {
					setTimeout( function () {
						createCommodityDetail( toCreate );
					}, 50 );  // 50 = something tiny; i.e., "reluinquish thread"
				}
			}

			$info.fadeOut( 'fast', function ( ) {
				// these steps are crucial: the Detail Controls are bound to the
				// $info element, so it must be removed for GC.  We then recreate
				// it, and accordingly set the closure variable ($info)
				var $newInfo = $('<div>', {id: 'commodity_detail'} );
				$newInfo.css('display', 'none');
				$info.replaceWith( $newInfo );
				$info = $newInfo.fadeIn();

				createCommodityDetail( coms );
			});
		};

		var $tables = $el.find('.items');

		var $tDemand   = $tables.filter('.demand').find('tbody');
		var $tEmission = $tables.filter('.emission').find('tbody');
		var $tPhysical = $tables.filter('.physical').find('tbody');

		$tDemand.selectable( {} );
		$tDemand.on( 'selectablestart', select_start );
		$tDemand.on( 'selectablestop', select_stop );
		$tEmission.selectable( {} );
		$tEmission.on( 'selectablestart', select_start );
		$tEmission.on( 'selectablestop', select_stop );
		$tPhysical.selectable( {} );
		$tPhysical.on( 'selectablestart', select_start );
		$tPhysical.on( 'selectablestop', select_stop );

	},
	create: function ( $el ) {
		var errors = {};
		var $form  = $el.closest('form');
		var $inputs = $form.find(':input');
		var data   = can.deparam( $form.serialize() );

		Temoa.fn.disable( $inputs );
		$form.find('.error').empty();  // remove any previous errors

		if ( Object.keys( errors ).length > 0 ) {
			// client-side checking for user convenience.  The server will check
			// for itself, of course.
			Temoa.fn.enable( $inputs );
			Temoa.fn.displayErrors( $form, errors );
			return;
		}

		this.analysis.attr( data ).save(
			function ( model ) {
				Temoa.fn.enable( $inputs );
				Temoa.fn.showStatus( 'Analysis successfully created.', 'info' );
		}, function ( xhr ) {
				Temoa.fn.enable( $inputs );
				if ( xhr && xhr.responseJSON ) {
					Temoa.fn.displayErrors( $form, xhr.responseJSON );
				}
		});
	},
	createNewCommodity: function ( CommodityObj, commodityOpts ) {
		var $newDiv = $('<div>', {id: 'commodity_detail'} );
		new CommodityDetail( $newDiv, {
			username: Temoa.fn.getCookie().username || null,
			analysis: this.analysis,
			commodity: new CommodityObj( commodityOpts )
		});
		$('#commodity_detail').replaceWith( $newDiv );
	},
	'#NewCommodityDemand click': function ( $el ) {
		var opts = {aId: this.analysis.id}
		this.createNewCommodity( AnalysisCommodityDemand, opts );
	},
	'#NewCommodityEmission click': function ( $el ) {
		var opts = {aId: this.analysis.id, name: 'New Emission Commodity'}
		this.createNewCommodity( AnalysisCommodityEmission, opts );
	},
	'#NewCommodityPhysical click': function ( $el ) {
		var opts = {aId: this.analysis.id, name: 'New Physical Commodity'}
		this.createNewCommodity( AnalysisCommodityPhysical, opts );
	},
	'[name="CommodityDemandRemove"] click': function ( $el, ev ) {
		$el.closest( 'tr' ).data('commodity').destroy();
	},
	'[name="CommodityEmissionRemove"] click': function ( $el, ev ) {
		$el.closest( 'tr' ).data('commodity').destroy();
	},
	'[name="CommodityPhysicalRemove"] click': function ( $el, ev ) {
		$el.closest( 'tr' ).data('commodity').destroy();
	},
	'{AnalysisCommodityDemand} created': function ( list, ev, commodity ) {
		this.analysis.commodity_demand.unshift( commodity.real_model );
	},
	'{AnalysisCommodityEmission} created' : function ( list, ev, commodity ) {
		this.analysis.commodity_emission.unshift( commodity.real_model );
	},
	'{AnalysisCommodityPhysical} created' : function ( list, ev, commodity ) {
		this.analysis.commodity_physical.unshift( commodity.real_model );
	},
});


can.Control('CommodityDetail', {
	defaults: {
			view: Temoa.C.ROOT_URL + '/client_template/analysis_commodity_detail.ejs'
		}
	},{
	init: function ( $el, options ) {
		var view = options.view;
		if ( Temoa.C.DEBUG )
			view += '?_=' + new Date().getTime();

		this.commodity = options.commodity;

		var view_opts = {
			username:   options.username || null,
			analysis:   options.analysis,
			commodity:  options.commodity
		};

		$el.append( can.view( view, view_opts ));
	},
	save: function ( $el ) {
		var errors = {};
		var $form  = $el.closest( 'form' );
		var inputs = $form.find(':input');
		var data   = can.deparam( $form.serialize() );

		Temoa.fn.disable( inputs );
		$form.find('.error').empty();  // remove any previous errors

		data.name = $.trim( data.name );
		if ( data.name.length < 1 ) {
			var msg = 'Please provide a name this commodity.';
			errors[ 'name' ] = [msg];
		}
		else if ( ! data.name.match( /^[A-z_]\w*$/ ) ) {
			var msg = 'Please only include alphanumeric characters, and begin ';
			msg += 'with a letter.  Note that this is used as an identifier in ';
			msg += 'the data file, so spaces are not valid.  If you understand ';
			msg += '"regular expressions", then follow the form ';
			msg += "'<code>[A-z_]\\w*<code>'.";
			errors[ 'name' ] = [msg];
		}

		if ( Object.keys( errors ).length > 0 ) {
			// client-side checking for user convenience.  The server will check
			// for itself, of course.
			Temoa.fn.enable( inputs );
			Temoa.fn.displayErrors( $form, errors );
			return;
		}

		var model = $el.closest('.commodity').data('commodity');

		// Use a 'saver' object to simulate atomicity. Only if there is success
		// do we update the model the UI is actually using.  Meanwhile, remove
		// the id before destroying the saver object (after we're done with it)
		// so as not to remove the object in the database.
		var saver = new model.constructor( model.attr() );
		saver.real_model = model;  // because {created} event recieves saver obj.

		saver.attr( data ).save(
			function ( updated_model ) {
				Temoa.fn.enable( inputs );
				model.attr( updated_model.attr() );  // "atomically" update

				saver.real_model = null;
				saver.attr( {id: null} ).destroy();  // don't delete in DB

				Temoa.fn.showStatus('Saved!', 'info' );
			}, function ( xhr ) {
				Temoa.fn.enable( inputs );
				saver.attr({id: null}).destroy();  // don't delete in DB

				if ( xhr && xhr.responseJSON ) {
					Temoa.fn.displayErrors( $form, xhr.responseJSON );
				}
		});
	},
	'[name="CommoditiesCancel"] click': function ( $el, ev ) {
		var $block = $el.closest('.commodity');
		var c = $block.data('process');
		$block.find('[name="name"]').val( c.attr('name') || '' );
	},
	'[name="CommoditiesUpdate"] click': function ( $el, ev ) {
		this.save( $el );
	},
	'[name="CommoditiesCreate"] click': function ( $el, ev ) {
		this.save( $el );
	},
	'input keyup': function ( $el, ev ) {
		if ( 13 === ev.keyCode ) { // 13 == enter
			this.save( $(ev.target) );
		}
	},
	'{AnalysisCommodityDemand} destroyed': function ( Model, ev, commodity ) {
		if ( this.commodity === commodity ) {
			var $div = this.element.find( '#CommodityForm_' + commodity.id );
			$div.remove();
		}
	},
	'{AnalysisCommodityEmission} destroyed': function ( Model, ev, commodity ) {
		if ( this.commodity === commodity ) {
			var $div = this.element.find( '#CommodityForm_' + commodity.id );
			$div.remove();
		}
	},
	'{AnalysisCommodityPhysical} destroyed': function ( Model, ev, commodity ) {
		if ( this.commodity === commodity ) {
			var $div = this.element.find( '#CommodityForm_' + commodity.id );
			$div.remove();
		}
	}
});


can.Control('TechnologyCreate', {
	defaults: {
			view: Temoa.C.ROOT_URL + '/client_template/technology_create.ejs'
		}
	},{
	init: function ( $el, options ) {
		$el.hide();
	},
	create: function ( $el ) {
		var errors = {};
		var $form = $el.closest('form');
		var data = can.deparam( $form.serialize() );
		$form.find('.error').empty();  // remove any previous errors

		if ( ! data.name ) {
			errors['name'] = ['The new technology needs a name!'];
		}
		if ( ! data.capacity_to_activity ||
		            isNaN(Number( data.capacity_to_activity )) ) {
			var msg = 'Missing a CapacityToActivity factor.';
			errors['capacity_to_activity'] = [msg];
		}
		if ( ! data.description || data.description.length < 5 ) {
			var msg = 'Please provide at least a minimal description.';
			errors['description'] = [msg];
		}

		if ( Object.keys( errors ).length > 0 ) {
			// client-side checking, for speed.  The server will double check,
			// of course.
			Temoa.fn.displayErrors( $form, errors );
			return;
		}

		var control = this;
		this.technology.attr( data ).save( function ( model ) {
			control.hide();
		}, function ( xhr ) {
			if ( xhr && xhr.responseJSON ) {
				Temoa.fn.displayErrors( $form, xhr.responseJSON );
			}
		});
	},
	show: function ( ) {
		this.technology = new Technology();
		this.element.html( can.view( this.options.view ), {
			technology: this.technology
		});
		this.element.slideDown();
	},
	hide: function ( ) {
		var $el = this.element;
		$el.slideUp( function ( ) { $el.empty(); });
	},
	'[name="Create"] click': function ( $el ) {
		this.create( $el );
	},
	'[name="Cancel"] click': function ( $el ) {
		this.hide();
	},
	'{document} #NewTechnology click': function ( ) {
		this.show();
	},
	'input keyup': function ( $el, ev ) {
		if ( 13 == ev.keyCode ) { // 13 = enter
			this.create( $el );
		}
	}
});


can.Control('ProcessList', {
	defaults: {
			view: Temoa.C.ROOT_URL + '/client_template/process_list.ejs'
		}
	},{
	init: function ( $el, options ) {
		var view = options.view;
		if ( Temoa.C.DEBUG )
			view += '?_=' + new Date().getTime();

		var control = this;
		var analysis = options.analysis;
		this.analysis = analysis;

		can.when(
		  Process.findAll({aId: analysis.id}),
		  AnalysisTechnology.findAll({aId: analysis.id})
		).then( function(processes, technologies) {
			control.processes = processes;
			control.technologies = new can.Map();
			for ( var i = 0; i < technologies.length; ++i ) {
				control.technologies.attr( technologies[i].id, technologies[i] );
			}

			var _segFracs = {};  // use as map
			for ( var i = 0; i < analysis.segfracs.length; ++i ) {
				var sf = analysis.segfracs[ i ];
				_segFracs[ sf.id ] = sf;
			}

			// Unfortunately, CanJS is not smart enough to automatically link up
			// the various parts of the Temoa model.  Therefore we must do it
			// manually.  This is a benefit because it means there is only one
			// copy of various Constructors lying around (better for memory), and
			// means that if one gets updated, all references to it automatically
			// receive that update (single point of authority).  Luckily, this
			// set of for-loops is about it.  As an aside, it would be awful nice
			// if there were a _supported_ client side version of RDBMS
			// functionality.  However, it seems most browser developers are only
			// interested in NoSQL style functionality.  Sigh.
			for ( var i = 0; i < processes.length; ++i ) {
				var p = processes[ i ];
				var ea_list  = p.attr( 'emissionactivities' );
				var eff_list = p.attr( 'efficiencies' );

				p.attr( 'technology', control.technologies.attr( p.tId ));

				for ( var j = 0; j < ea_list.length; ++j ){
					var ea = ea_list[ j ];
					var eId = ea.attr('eId'); // efficiency id
					for ( var k = 0; k < eff_list.length; ++k ) {
						if ( eff_list[k].id === eId ) {
							ea.attr('efficiency', eff_list[k] )
						}
					}
				}
				for ( var cfi = 0; cfi < p.capacityfactors.length; ++cfi ) {
					var cf = p.capacityfactors[ cfi ];
					cf.attr( 'segfrac', _segFracs[ cf.sfId ] );
				}
			}

			for ( var i = 0; i < technologies.length; ++i ) {
				var t = technologies[ i ];
				for ( var cfi = 0; cfi < t.capacityfactors.length; ++cfi ) {
					var cf = t.capacityfactors[ cfi ];
					cf.attr( 'segfrac', _segFracs[ cf.sfId ] );
				}
			}

			var view_opts = {
				username:  Temoa.fn.getCookie().username || null,
				analysis:  analysis,
				processes: processes
			};

			// set up the autocomplete name options for new Process()es
			var new_process_names = new can.Map();
			var cur_process_names = {};
			for ( var i = 0; i < processes.length; ++i ) {
				var p = processes[ i ];
				cur_process_names[ p.technology.name + ', ' + p.vintage ] = true;
			}
			analysis.attr( 'new_process_names' , new_process_names );
			var vintages = analysis.vintages.split(/, */g);
			for ( var i = 0; i < activeTechnologyList.length; ++i ) {
				var tname = activeTechnologyList[ i ].name;
				for ( var j = 0; j < vintages.length; ++j ) {
					var pname = tname + ', ' + vintages[ j ];
					if ( cur_process_names[ pname ] )
						continue;

					new_process_names.attr( pname, pname );
				}
			}

			$el.append( can.view( view, view_opts ))
			$el.removeClass('hidden').fadeIn();
			$('#AnalysisProcessDetails').removeClass('hidden');
			$('#AnalysisTechnologyDetails').removeClass('hidden');

			var $tbody = $el.find('tbody');
			$tbody.selectable( {} )
			$tbody.on( 'selectablestart', function () {
				$('#AnalysisProcessDetails .items').fadeOut();
			});
			$tbody.on( 'selectablestop', function () {
				function createProcessDetail ( p, delay ) {
					setTimeout( function () {
						// It is crucial to attach to removable div, for later GC
						var $div = $('<div>', {id: 'ProcessDetail_' + p.id});
						view_opts['process'] = p;
						new ProcessDetail( $div, view_opts );
						$pcItems.append( $div );  // add to DOM /after/ creation
					}, delay );
				}

				function createAnalysisTechnologyDetail ( t, delay ) {
					setTimeout( function () {
						// It is crucial to attach to removable div, for later GC
						var $div = $('<div>', {id: 'AnalysisTechnologyDetail_' + t.id});
						view_opts['technology'] = t;
						new AnalysisTechnologyDetail( $div, view_opts );
						$tcItems.append( $div );  // add to DOM /after/ creation
					}, delay );
				}

				var $sel = $( this ).find( 'tr.ui-selected' );

				var to_display = new Array();
				var ids        = new Array();
				var a_techs    = {}; // use as a set() object.
				for ( var i = 0; i < $sel.length; ++i ) {
					var p = $($sel[i]).data().process;
					to_display.push( p );
					ids.push( p.id );
					a_techs[ p.tId ] = p.technology;
				}

				ids.sort( Temoa.fn.numericSort );
				var $cookie = Temoa.fn.getCookie();
				$cookie.process_ids = ids;
				Temoa.fn.setCookie( $cookie );

				var $pcItems = $('#AnalysisProcessDetails .items');
				var $tcItems = $('#AnalysisTechnologyDetails .items');

				if ( ! to_display.length ) {
					// Nothing to display.  If the first child is a new process,
					// then remove all others, but leave it.
					var children = $pcItems.children();
					if ( children.length ) {
						var first_child = $(children[0]).find('.process');
						if ( first_child.data('process').isNew() ) {
							$pcItems.children().not( children[0] ).remove();
							$pcItems.fadeIn();
						} else {
							$pcItems.empty();
						}
					}
				} else { // something to display
					var view_opts = {
						analysis: analysis,
						username: Temoa.fn.getCookie().username || null
					}

					// remove any child divs so browser can GC.
					$pcItems.empty().fadeIn();
					$tcItems.empty().fadeIn();;

					// Wrap the actual creation within a setTimeout list traversal
					// so that each process detail block can display when it's ready.
					// This way, the user will immediately see results, even for
					// large selections.  This also presents a graduated fade-in
					// effect that some may find pleasing.
					for ( var i = 0; i < to_display.length; ++i ) {
						createProcessDetail( to_display[ i ], 50 * i );
						// 50 = something tiny; "relinquish thread"
					}
					for ( var i in a_techs ) {
						createAnalysisTechnologyDetail( a_techs[ i ], 50 * i );
						// 50 = something tiny; "relinquish thread"
					}
				}
			});

			// Pre-select what was selected in this session.
			// (Handy if the page needs to reload.)
			var $cookie = Temoa.fn.getCookie();
			if ( $cookie.process_ids ) {
				var ids = $cookie.process_ids;

				var sel = '[data-id="' + ids.join('"],[data-id="') + '"]';
				$tbody.find( sel ).addClass('ui-selected');
				$tbody.trigger('selectablestop')
			}

			$('#ProcessList').data('processes', processes);

		}, function ( error ) {
			console.log( error );
			Temoa.fn.showStatus( 'An unknown error occurred while collecting analysis ' +
			  'processes and technologies.  If after a fresh page reload (e.g. ' +
			  'close and reopen your browser) this message still occurs, ' +
			  'please let the Temoa Project know about it.  Debugging ' +
			  'message is: ' + error );
		});
	},
	'#NewProcessButton click': function ( $el, ev ) {
		var $tabs = $('#AnalysisProcessDetails .items > div > table');
		if ( $tabs.length && $($tabs[0]).data('process').isNew() ) {
			return;
		}
		var $div = $('<div>', {id: 'NewProcess'});
		new ProcessDetail( $div, {
			username: Temoa.fn.getCookie().username || null,
			process: new Process({aId: this.analysis.id}),
			analysis: this.analysis
		});
		$('#AnalysisProcessDetails .items').prepend( $div ).fadeIn();
	},
	'[name="ProcessRemove"] click': function ( $el, ev ) {
		var p = $el.closest( 'tr' ).data('process');

		// cleanup any dangling references to this process in the WUI
		$( '#ProcessDetail_' + p.id ).remove()

		p.destroy(); // finally, actually delete it on the server
	},
	'{Process} created': function ( list, ev, obj ) {
		var control      = this;
		var new_process  = obj.real_model;
		var processes    = this.processes;
		var technologies = this.technologies;
		var tech = technologies.attr( obj.tId );

		if ( ! new_process.capacityfactors )
			new_process.attr('capacityfactors', new ProcessCapacityFactor.List() );
		if ( ! new_process.costsfixed )
			new_process.attr('costsfixed', new ProcessCostFixed.List() );
		if ( ! new_process.costsvariable )
			new_process.attr('costsvariable', new ProcessCostVariable.List() );
		if ( ! new_process.efficiencies )
			new_process.attr('efficiencies', new ProcessEfficiency.List() );
		if ( ! new_process.emissionactivities )
			new_process.attr('emissionactivities',
			  new ProcessEmissionActivity.List() );

		// The new process needs the template to be reprocessed.  Live binding
		// is currently only partially usable, working only if directly
		// attached to the DOM.  Wrapper code like '<% if ... %>' does not appear
		// to get reprocessed automatically.
		$('#NewProcess').remove();
		setTimeout( function ( ) {
			if ( ! tech ) {
				// Technology was not in our list: add it
				tech = new_process.attr('technology');
				technologies.attr(tech.id, tech);
			} else {
				// Technology already in our list; now update it with any new info
				tech.attr( new_process.technology.attr() );
				new_process.attr('technology', tech);
			}
			var $div = $('<div>', {id: 'ProcessDetail_' + obj.id});
			new ProcessDetail( $div, {
				username: Temoa.fn.getCookie().username || null,
				process: new_process,
				analysis: control.analysis
			});
			$('#AnalysisProcessDetails .items').prepend( $div );
			processes.unshift( new_process );
		}, 20 );
	},
	'{ProcessEmissionActivity} created': function ( list, ev, obj ) {
		var control = this;
		var new_ea  = obj.real_model;

		// The procprocessess template needs to be reprocessed.  Live binding is
		// currently only partially usable, working only if directly
		// attached to the DOM.  Wrapper code like '<% if ... %>' does not appear
		// to get reprocessed automatically.  So, replace the div in question.
		setTimeout( function ( ) {
			// necessary to do this work after a minor wait so that the new_ea
			// has a chance to update itself.  e.g., the pId and eId.
			var pId  = new_ea.pId;
			var eId  = new_ea.eId;
			var sel  = '#ProcessDetail_' + pId;
			var $div = $('<div>', {id: 'ProcessDetail_' + pId});
			var p    = $( sel ).find('.process').data('process');

			for ( var i = 0; i < p.efficiencies.length; ++i ) {
				if ( p.efficiencies[ i ].id === eId )
					new_ea.attr('efficiency', p.efficiencies[ i ] );
			}

			new ProcessDetail( $div, {
				username: Temoa.fn.getCookie().username || null,
				process: p,
				analysis: control.analysis
			});
			$( sel ).replaceWith( $div );
		}, 20 );
	},
	'{ProcessCapacityFactor} created': function ( list, ev, obj ) {
		var segfracs = this.options.analysis.segfracs;
		for ( var i = 0; i < segfracs.length; ++i ) {
			if ( segfracs[ i ].id === obj.sfId )
				obj.attr('segfrac', segfracs[ i ] );
		}
	},
	'{ProcessCostFixed} created': function ( list, ev, obj ) {
		var control = this;
		var new_cf  = obj.real_model;

		// The process template needs to be reprocessed.  Live binding is
		// currently only partially usable, working only if directly
		// attached to the DOM.  Wrapper code like '<% if ... %>' does not appear
		// to get reprocessed automatically.  So, replace the div in question.
		setTimeout( function ( ) {
			// necessary to do this work after a minor wait so that the new_cf
			// has a chance to update itself.  e.g., the pId would otherwise be
			// null.
			var pId  = new_cf.pId;
			var sel  = '#ProcessDetail_' + pId;
			var $div = $('<div>', {id: 'ProcessDetail_' + pId});
			var p    = $( sel ).find('.process').data('process');

			new ProcessDetail( $div, {
				username: Temoa.fn.getCookie().username || null,
				process: p,
				analysis: control.analysis
			});
			$( sel ).replaceWith( $div );
		}, 20 );
	},
	'{ProcessCostVariable} created': function ( list, ev, obj ) {
		var control = this;
		var new_cv  = obj.real_model;

		// The process template needs to be reprocessed.  Live binding is
		// currently only partially usable, working only if directly
		// attached to the DOM.  Wrapper code like '<% if ... %>' does not appear
		// to get reprocessed automatically.  So, replace the div in question.
		setTimeout( function ( ) {
			// necessary to do this work after a minor wait so that the new_cv
			// has a chance to update itself.  e.g., the pId would otherwise be
			// null.
			var pId  = new_cv.pId;
			var sel  = '#ProcessDetail_' + pId;
			var $div = $('<div>', {id: 'ProcessDetail_' + pId});
			var p    = $( sel ).find('.process').data('process');

			new ProcessDetail( $div, {
				username: Temoa.fn.getCookie().username || null,
				process: p,
				analysis: control.analysis
			});
			$( sel ).replaceWith( $div );
		}, 20 );
	},
});


can.Control('ProcessDetail', {
	defaults: {
			view: Temoa.C.ROOT_URL + '/client_template/process_detail.ejs',
		}
	},{
	init: function ( $el, options ) {  // ProcessDetail
		var view = options.view;
		if ( Temoa.C.DEBUG )
			view += '?_=' + new Date().getTime();

		var p = options.process;

		if ( ! p.capacityfactors )
			p.attr('capacityfactors', new ProcessCapacityFactor.List());
		if ( ! p.costsfixed )
			p.attr('costsfixed', new ProcessCostFixed.List());
		if ( ! p.costsvariable )
			p.attr('costsvariable', new ProcessCostVariable.List());
		if ( ! p.efficiencies )
			p.attr('efficiencies', new ProcessEfficiency.List());
		if ( ! p.emissionactivities )
			p.attr('emissionactivities',
			  new ProcessEmissionActivity.List());
		if ( ! p.analysis )
			p.attr('analysis', options.analysis );

		var view_opts = {
			username: options.username || null,
			analysis: options.analysis,
			process:  p
		};

		$el.append( can.view( view, view_opts ));

		var $tbody = $el.find('.process:first tbody');
	},
	destroy: function ( ) {  // ProcessDetail
		var e = this.options.process.efficiencies;
		var ea = this.options.process.emissionactivities;
		if ( e && e.length && e[0].isNew() ) e[0].destroy();
		if ( ea && ea.length && ea[0].isNew() ) ea[0].destroy();

		can.Control.prototype.destroy.call(this);
	},
	save: function ( $el ) {  // ProcessDetail
		var errors = {}
		  , $pForm   = null, pData   = null
		  , $cfpForm = null, cfpData = null    // cfp = Capacity Factor Process
		  , $cfForm  = null, cfData  = null
		  , $cvForm  = null, cvData  = null
		  , $effForm = null, effData = null
		  , $emForm  = null, emData  = null
		  , check_for_save = new Array()
		  , to_save = new Array();
		var $pTable = $el.closest('.process');

		// don't collect any inputs that might be disabled for other reasons
		// (like the delete buttons)
		var $inputs = $pTable.find(':input').not('[disabled="disabled"]');
		var process = $pTable.data('process');
		var pId = process.attr('id');

		if ( pId ) {
			// i.e., process already exists in DB
			$pForm   = $('#Process_' + pId);
			$cfpForm = $('#ProcessCapacityFactors_' + pId);
			$cfForm  = $('#ProcessCostsFixed_' + pId );
			$cvForm  = $('#ProcessCostsVariable_' + pId );
			$effForm = $('#ProcessEfficiencies_' + pId );
			$emForm  = $('#ProcessEmissionActivities_' + pId );
		} else {
			$pForm = $('#NewProcessForm');
		}

		$pTable.find('.error').empty(); // remove any previous error messages

		// 1. Collect the data
		if ( $pForm )
			pData = can.deparam( $pForm.serialize() );
		if ( $cfpForm )
			cfpData = can.deparam( $cfpForm.serialize() );
		if ( $cfForm )
			cfData = can.deparam( $cfForm.serialize() );
		if ( $cvForm )
			cvData = can.deparam( $cvForm.serialize() );
		if ( $effForm )
			effData = can.deparam( $effForm.serialize() );
		if ( $emForm )
			emData = can.deparam( $emForm.serialize() );

		// 2. Try to ensure user doesn't make a change while we're saving.  This
		//    will normally not be a problem given a fast-enough network
		//    connection, but "just in case" there's a hangup.  Don't forget to
		//    enable( $inputs ) once any computation is complete (e.g. an error
		//    occurs, or we've successfully saved the data).
		Temoa.fn.disable( $inputs );

		// 3. First check the data and queue each can.Model for saving
		if ( process.isNew() ) {
			if ( ! pData.name.match( /^[A-z_]\w*, *-?\d+$/ ) ) {
				var msg = 'The process name must follow the form "technology, ';
				msg += 'vintage".  If you are unsure of valid names, press the up ';
				msg += 'or down arrow keys while this field has focus (has the ';
				msg += 'blinking cursor), and a list of options should appear.';
				errors['name'] = [msg];
			}
		} else {
			// Process
			if ( pData.discountrate && isNaN(Number(pData.discountrate)) ) {
				var msg = 'Please specify a numeric discount rate or leave blank.';
				errors['discountrate'] = [msg];
			}

			if ( pData.lifetime ) {
				if ( isNaN(Number(pData.lifetime)) ) {
					var msg = 'Please specify a positive number or leave blank.';
					errors['lifetime'] = [msg];
				} else if ( Number(pData.lifetime) <= 0 ) {
					var msg = 'Please specify a positive number or leave blank.';
					errors['lifetime'] = [msg];
				}
			}

			if ( pData.loanlife ) {
				if ( isNaN(Number(pData.loanlife)) ) {
					var msg = 'Please specify a positive number or leave blank.';
					errors['loanlife'] = [msg];
				} else if ( Number(pData.loanlife) <= 0 ) {
					var msg = 'Please specify a positive number or leave blank.';
					errors['loanlife'] = [msg];
				}
			}

			if ( pData.costinvest && isNaN(Number(pData.costinvest)) ) {
				var msg = 'Please specify a number or leave blank.';
				errors['costinvest'] = [msg];
			}

			if ( pData.existingcapacity ) {
				if ( isNaN(Number(pData.existingcapacity)) ) {
					var msg = 'Please specify a positive number or leave blank.';
					errors['existingcapacity'] = [msg];
				} else if ( Number(pData.existingcapacity) <= 0 ) {
					var msg = 'Please specify a positive number or leave blank.';
					errors['existingcapacity'] = [msg];
				}
			}

			// Efficiency
			var eNewInp = $.trim(effData.EfficiencyNew_inp)
			  , eNewOut = $.trim(effData.EfficiencyNew_out)
			  , eNewVal = $.trim(effData.EfficiencyNew_value);
			if ( eNewInp.length || eNewOut.length || eNewVal.length ) {
				if ( ! (eNewInp.length && eNewOut.length && eNewVal.length) ) {
					var msg = 'If you specify a new efficiency, you need to ';
					msg += 'specify all three of input, output, and a new value.';
					errors['General Error'] = [msg];
				}
				if ( isNaN(Number(eNewVal)) ) {
					var msg = 'Please specify a number.';
					errors['EfficiencyNew_value'] = [msg];
				}
				if ( ! eNewInp.match( /^[A-z_]\w*$/ ) ) {
					var msg = 'Invalid commodity name.  If you are unsure of what ';
					msg += 'to put here, press the up or down arrow keys while ';
					msg += 'this field has focus (has the blinking cursor), and a ';
					msg += 'list of options should appear.';
					errors['EfficiencyNew_inp'] = [msg];
				}
				if ( ! eNewOut.match( /^[A-z_]\w*$/ ) ) {
					var msg = 'Invalid commodity name.  If you are unsure of what ';
					msg += 'to put here, press the up or down arrow keys while ';
					msg += 'this field has focus (has the blinking cursor), and a ';
					msg += 'list of options should appear.';
					errors['EfficiencyNew_out'] = [msg];
				}
			}

			// EmissionActivity
			var emNewPol = $.trim(emData.EmissionActivityNew_pol)
			  , emNewEff = $.trim(emData.EmissionActivityNew_eff)
			  , emNewVal = $.trim(emData.EmissionActivityNew_value);
			if ( emNewPol.length || emNewEff.length || emNewVal.length ) {
				if ( ! (emNewPol.length && emNewEff.length && emNewVal.length) ) {
					var msg = 'If adding a new emission activity, you need to ';
					msg += 'specify all three fields.  You may also use the Shift ';
					msg += 'to remove the row, or simply select another process.';
					errors['General Error'] = [msg];
				}
				if ( isNaN(Number(emNewVal)) ) {
					var msg = 'Please specify a number.';
					errors['EmissionActivityNew_value'] = [msg];
				}
				if ( ! emNewPol.match( /^[A-z_]\w*$/ ) ) {
					var msg = 'Invalid commodity name.  This field expects the ';
					msg += 'name of an emission commodity.  If you are unsure of ';
					msg += 'what to put here, press the up or down arrow keys ';
					msg += 'while this field has focus (has the blinking cursor), ';
					msg += 'and a list of options should appear.';
					errors['EmissionActivityNew_pol'] = [msg];
				}
				if ( ! emNewEff.match( /^[A-z_]\w*, *[A-z_]\w*$/ ) ) {
					var msg = 'Invalid efficiency description.  This field expects ';
					msg += 'a comma-separated "[input], [output]" specification of ';
					msg += '<em>which</em> efficiency flow this emission activity ';
					msg += 'will follow.  If you are unsure of what to put here, ';
					msg += 'press the up or down arrow keys while this field has ';
					msg += 'focus (has the blinking cursor), and a list of options ';
					msg += 'should appear.';
					errors['EmissionActivityNew_eff'] = [msg];
				}
			}

			// Capacity Factor
			var cfpNewTS  = $.trim(cfpData.CapacityFactorProcessNew_timeslice)
			  , cfpNewVal = $.trim(cfpData.CapacityFactorProcessNew_value);
			if ( cfpNewTS.length || cfpNewVal.length ) {
				if ( ! (cfpNewTS.length && cfpNewVal.length) ) {
					var msg = 'If you specify either field of a Capacity Factor, ';
					msg += 'you need to fill out both fields.  If you would rather ';
					msg += 'cancel, click anywhere outside of a field (so no ';
					msg += 'fields have focus), and push Shift to display the red ';
					msg += '"Cancel" button.';
					errors['General Error'] = [msg];
				}
				if ( isNaN(Number(cfpNewVal)) ) {
					var msg = 'Please specify a number.';
					errors['CapacityFactorTechNew_value'] = [msg];
				}
				if ( ! cfpNewTS.match( /^[A-z_]\w*, *[A-z_]\w*$/ ) ) {
					var msg = 'Invalid timeslice name.  If you are unsure of what ';
					msg += 'to put here, press the up or down arrow keys while ';
					msg += 'this field has focus (has the blinking cursor), and a ';
					msg += 'list of options should appear.';
					errors['CapacityFactorProcessNew_timeslice'] = [msg];
				}
			}

			// CostFixed
			var cfNewPer = $.trim(cfData.CostFixedNew_per)
			  , cfNewVal = $.trim(cfData.CostFixedNew_value);
			if ( cfNewPer.length || cfNewVal.length ) {
				if ( ! (cfNewPer.length && cfNewVal.length) ) {
					var msg = 'If adding a new fixed costs, you need to specify ';
					msg += 'both fields.  If you are trying to remove it, you may ';
					msg += 'use the Shift key to delete the row, or simply select ';
					errors['General Error'] = [msg];
				}
				if ( isNaN(Number(cfNewVal)) ) {
					var msg = 'Please specify a number.';
					errors['CostFixedNew_value'] = [msg];
				}
				if ( ! cfNewPer.match( /^-?\d+$/ ) ) {
					var msg = 'Invalid period.  This field expects one of the ';
					msg += 'analysis vintages.  Note that the final year is not a ';
					msg += 'valid vintage.  See the Temoa Documentation for more ';
					msg += 'information on this detail.';
					errors['CostFixedNew_per'] = [msg];
				}
			}

			// CostVariable
			var cvNewPer = $.trim(cvData.CostVariableNew_per)
			  , cvNewVal = $.trim(cvData.CostVariableNew_value);
			if ( cvNewPer.length || cvNewVal.length ) {
				if ( ! (cvNewPer.length && cvNewVal.length) ) {
					var msg = 'If adding a new variable costs, you need to specify ';
					msg += 'both fields.  If you are trying to remove it, you may ';
					msg += 'use the Shift key to delete the row, or simply select ';
					errors['General Error'] = [msg];
				}
				if ( isNaN(Number(cvNewVal)) ) {
					var msg = 'Please specify a number.';
					errors['CostVariableNew_value'] = [msg];
				}
				if ( ! cvNewPer.match( /^-?\d+$/ ) ) {
					var msg = 'Invalid period.  This field expects one of the ';
					msg += 'analysis vintages.  Note that the final year is not a ';
					msg += 'valid vintage.  See the Temoa Documentation for more ';
					msg += 'information on this detail.';
					errors['CostVariableNew_per'] = [msg];
				}
			}
		}

		if ( Object.keys( errors ).length > 0 ) {
			// client-side checking for user convenience.  The server will check
			// for itself, of course.
			Temoa.fn.enable( $inputs );
			Temoa.fn.displayErrors( $pTable, errors );
			return;
		}

		// client side error checking complete.
		check_for_save.push( [process, pData] );

		for ( var name in cfpData ) {
			var sel = '[name="' + name + '"]';
			if ( name.match(/^CapacityFactorProcessNew/) ) {
				if ( name.match( /_timeslice$/ ) ) {
					var cf = $pTable.find( sel ).closest('tr').data('capacityfactor');
					to_save.push( [cf, {
					  timeslice: cfpData.CapacityFactorProcessNew_timeslice,
					  value:     cfpData.CapacityFactorProcessNew_value,
					}]);
				}
			} else if ( name.match(/^CapacityFactorProcess_\d+$/) ) {
				var cf = $pTable.find( sel ).closest('tr').data('capacityfactor');
				to_save.push( [cf, {value: cfpData[ name ]}] );
			}
		}

		for ( var name in cfData ) {
			var sel = '[name="' + name + '"]';
			if ( name.match(/^CostFixedNew/) ) {
				if ( name.match( /_per$/ ) ) {
					var cf = $pTable.find( sel ).closest('tr').data('costfixed');
					check_for_save.push( [cf, {
					  per:   cfData.CostFixedNew_per,
					  value: cfData.CostFixedNew_value,
					}]);
				}
			} else if ( name.match(/^CostFixed_\d+$/) ) {
				var cf = $pTable.find( sel ).closest('tr').data('costfixed');
				check_for_save.push( [cf, {value: cfData[ name ]}] );
			}
		}

		for ( var name in cvData ) {
			var sel = '[name="' + name + '"]';
			if ( name.match(/^CostVariableNew/) ) {
				if ( name.match( /_per$/ ) ) {
					var cv = $pTable.find( sel ).closest('tr').data('costvariable');
					check_for_save.push( [cv, {
					  per:   cvData.CostVariableNew_per,
					  value: cvData.CostVariableNew_value,
					}]);
				}
			} else if ( name.match(/^CostVariable_\d+$/) ) {
				var cv = $pTable.find( sel ).closest('tr').data('costvariable');
				check_for_save.push( [cv, {value: cvData[ name ]}] );
			}
		}

		for ( var name in effData ) {
			var sel = '[name="' + name + '"]';
			if ( name.match(/^EfficiencyNew/) ) {
				if ( name.match( /_inp$/ ) ) {
					var eff = $pTable.find( sel ).closest('tr').data('efficiency');
					check_for_save.push( [eff, {
					  inp:   effData.EfficiencyNew_inp,
					  out:   effData.EfficiencyNew_out,
					  value: effData.EfficiencyNew_value,
					}]);
				}
			} else if ( name.match(/^Efficiency_\d+$/) ) {
				var eff = $pTable.find( sel ).closest('tr').data('efficiency');
				check_for_save.push( [eff, {value: effData[ name ]}] );
			}
		}

		for ( var name in emData ) {
			var sel = '[name="' + name + '"]';
			if ( name.match(/^EmissionActivityNew/) ) {
				if ( name.match( /_pol$/ ) ) {
					var ema = $pTable.find( sel ).closest('tr').data('emissionactivity');
					check_for_save.push( [ema, {
					  pol:   emData.EmissionActivityNew_pol,
					  eff:   emData.EmissionActivityNew_eff,
					  value: emData.EmissionActivityNew_value,
					}]);
				}
			} else if ( name.match(/^EmissionActivity_\d+$/) ) {
				var ema = $pTable.find( sel ).closest('tr').data('emissionactivity');
				check_for_save.push( [ema, {value: emData[ name ]}] );
			}
		}

		for ( var i in check_for_save ) {
			var model = check_for_save[ i ][ 0 ];
			var data  = check_for_save[ i ][ 1 ];

			for ( var name in data ) {
				if ( ('' === data[ name ] && null == model[ name ])
				    || (data[ name ] == model[ name ] ) )
				{ // intentionally only one triple equals; compare "1" and 1 equal
					delete data[ name ];
				}
			}
			if ( Object.keys( data ).length === 0 ) {
				delete check_for_save[ i ];  // intentially leave as 'undefined'
			}
		}

		  // Only save the values that have not changed, if any
		for ( var i in check_for_save ) {
			if ( check_for_save[ i ] ) {
				to_save.push( check_for_save[ i ] );
			}
		}

		Temoa.fn.save_to_server({ to_save: to_save, inputs: $inputs, display: $pTable });

	},
	'[name="ProcessCancel"] click': function ( $el, ev ) {  // ProcessDetail
		var $block = $el.closest('.process');
		var p = $block.data('process');

		if ( p !== this.options.process )
			return;

		if ( p.isNew() ) {
			this.element.remove();
			return;
		}

		$block.find('[name="discountrate"]').val( p.attr('discountrate') || '' );
		$block.find('[name="lifetime"]').val( p.attr('lifetime') || '' );
		$block.find('[name="loanlife"]').val( p.attr('loanlife') || '' );
		$block.find('[name="existingcapacity"]').val( p.attr('existingcapacity') || '' );
		$block.find('[name="costinvest"]').val( p.attr('costinvest') || '' );

		var capfac = this.options.process.capacityfactors;
		var cf = this.options.process.costsfixed;
		var cv = this.options.process.costsvariable;
		var e = this.options.process.efficiencies;
		var ea = this.options.process.emissionactivities;
		if ( capfac && capffac.length && capfac[0].isNew() ) capfac[0].destroy();
		if ( cf && cf.length && cf[0].isNew() ) cf[0].destroy();
		if ( cv && cv.length && cv[0].isNew() ) cv[0].destroy();
		if ( e && e.length && e[0].isNew() ) e[0].destroy();
		if ( ea && ea.length && ea[0].isNew() ) ea[0].destroy();
	},
	'[name="ProcessUpdate"] click': function ( $el, ev ) {  // ProcessDetail
		this.save( $el );
	},
	'[name="ProcessCreate"] click': function ( $el, ev ) {  // ProcessDetail
		this.save( $el );
	},
	'input keyup': function ( $el, ev ) {  // ProcessDetail
		if ( 13 === ev.keyCode ) { // 13 == enter
			this.save( $(ev.target) );
		}
	},
	'[name="AddCapacityFactorProcess"] click': function ( $el, ev ) {  // ProcessDetail
		var cf_list = this.options.process.capacityfactors;
		if ( cf_list && cf_list.length && cf_list[0].isNew() ) {
			// only one new process at a time.
			return;
		}

		var tOpts = this.options;
		var opts = { aId: tOpts.analysis.id, pId: tOpts.process.id };
		var newCapacityFactor = new ProcessCapacityFactor( opts );
		cf_list.unshift( newCapacityFactor );
	},
	'[name="AddCostFixed"] click': function ( $el, ev ) {  // ProcessDetail
		var cf_list = this.options.process.costsfixed;
		if ( cf_list && cf_list.length && cf_list[0].isNew() ) {
			// only one new process at a time.
			return;
		}

		var tOpts = this.options;
		var opts = { aId: tOpts.analysis.id, pId: tOpts.process.id };
		var newCostFixed = new ProcessCostFixed( opts );
		cf_list.unshift( newCostFixed );
	},
	'[name="AddCostVariable"] click': function ( $el, ev ) {  // ProcessDetail
		var cv_list = this.options.process.costsvariable;
		if ( cv_list && cv_list.length && cv_list[0].isNew() ) {
			// only one new process at a time.
			return;
		}

		var tOpts = this.options;
		var opts = { aId: tOpts.analysis.id, pId: tOpts.process.id };
		var newCostVariable = new ProcessCostVariable( opts );
		cv_list.unshift( newCostVariable );
	},
	'[name="AddEfficiency"] click': function ( $el, ev ) {  // ProcessDetail
		var e_list = this.options.process.efficiencies;
		if ( e_list && e_list.length && e_list[0].isNew() ) {
			// only one new process at a time.
			return;
		}

		var tOpts = this.options;
		var opts = { aId: tOpts.analysis.id, pId: tOpts.process.id };
		var newEff = new ProcessEfficiency( opts );
		e_list.unshift( newEff );
	},
	'[name="AddEmissionActivity"] click': function ( $el, ev ) { // ProcessDetail
		var ea_list = this.options.process.emissionactivities;
		if ( ea_list && ea_list.length && ea_list[0].isNew() ) {
			// only one new process at a time.
			return;
		}

		var tOpts = this.options;
		var opts = { aId: tOpts.analysis.id, pId: tOpts.process.id };
		var newEma = new ProcessEmissionActivity( opts );
		ea_list.unshift( newEma );
	},
	'[name="CapacityFactorProcessRemove"] click': function ( $el, ev ) { // ProcessDetail
		$el.closest( 'tr' ).data('capacityfactor').destroy();
	},
	'[name="CostFixedRemove"] click': function ( $el, ev ) { // ProcessDetail
		$el.closest( 'tr' ).data('costfixed').destroy();
	},
	'[name="CostVariableRemove"] click': function ( $el, ev ) { // ProcessDetail
		$el.closest( 'tr' ).data('costvariable').destroy();
	},
	'[name="EfficiencyRemove"] click': function ( $el, ev ) { // ProcessDetail
		var e = $el.closest( 'tr' ).data('efficiency');
		var p = this.options.process;
		var ea_list = p.emissionactivities;

		// Cleanup attached EmissionActivities
		for ( var i = 0; i < ea_list.length; ++i ) {
			var ea = ea_list[ i ];
			if ( ea.eId === e.id )
				ea.attr('id', null).destroy();
		}

		e.destroy();
	},
	'[name="EmissionActivityRemove"] click': function ( $el, ev ) { // ProcessDetail
		$el.closest( 'tr' ).data('emissionactivity').destroy();
	},
});


can.Control('AnalysisTechnologyDetail', {
	defaults: {
			view: Temoa.C.ROOT_URL + '/client_template/analysis_technology_detail.ejs',
		}
	},{
	init: function ( $el, options ) {  // AnalysisTechnologyDetail
		var view = options.view;
		if ( Temoa.C.DEBUG )
			view += '?_=' + new Date().getTime();

		var t = options.technology;

		if ( ! t.capacityfactors )
			t.attr('capacityfactors', new AnalysisTechnologyCapacityFactor.List());
		if ( ! t.inputsplits )
			t.attr('inputsplits', new AnalysisTechnologyInputSplit.List());
		if ( ! t.outputsplits )
			t.attr('outputsplits', new AnalysisTechnologyOutputSplit.List());

		var view_opts = {
			username:   options.username || null,
			analysis:   options.analysis,
			technology: t
		};

		$el.append( can.view( view, view_opts ));
	},
	destroy: function ( ) {  // AnalysisTechnologyDetail
		var capfac_list = this.options.technology.capacityfactors;
		var is_list = this.options.technology.inputsplits;
		var os_list = this.options.technology.outputsplits;
		if ( capfac_list && capfac_list.length && capfac_list[0].isNew() )
			capfac_list[0].destroy();
		if ( is_list && is_list.length && is_list[0].isNew() )
			is_list[0].destroy();
		if ( os_list && os_list.length && os_list[0].isNew() )
			os_list[0].destroy();

		can.Control.prototype.destroy.call(this);
	},
	save: function ( $el ) {  // AnalysisTechnologyDetail
		var errors = {}
		  , $tForm  = null, tData  = null
		  , $cfForm = null, cfData = null
		  , $isForm = null, isData = null
		  , $osForm = null, osData = null
		  , to_save = new Array();
		var $tTable = $el.closest('.technology');

		// don't collect any inputs that might be disabled for other reasons
		// (like the delete buttons)
		var $inputs = $tTable.find(':input').not('[disabled="disabled"]');
		var tech = $tTable.data('technology');
		var tId = tech.attr('id');

		if ( tId ) {
			$tForm  = $('#FormTechnology_' + tId);
			$cfForm = $('#FormTechnologyCapacityFactors_' + tId);
			$isForm = $('#FormTechnologyInputSplits_' + tId);
			$osForm = $('#FormTechnologyOutputSplits_' + tId);
		} else {
			$tForm = $('#NewTechnologyForm');
		}

		$tTable.find('.error').empty(); // remove any previous error messages

		// 1. Collect the data
		if ( $tForm )
			tData = can.deparam( $tForm.serialize() );
		if ( $cfForm )
			cfData = can.deparam( $cfForm.serialize() );
		if ( $isForm )
			isData = can.deparam( $isForm.serialize() );
		if ( $osForm )
			osData = can.deparam( $osForm.serialize() );

		// 2. Try to ensure user doesn't make a change while we're saving.  This
		//    will normally not be a problem given a fast-enough network
		//    connection, but "just in case" there's a hangup.  Don't forget to
		//    enable( $inputs ) once any computation is complete (e.g. an error
		//    occurs, or we've successfully saved the data).
		Temoa.fn.disable( $inputs );

		// 3. First check the data and queue each can.Model for saving
		if ( tech.isNew() ) {
			if ( ! tData.name.match( /^[A-z_]\w*$/ ) ) {
				var msg = 'The technology name must begin with a letter and only ';
				msg += 'use alphanumerics.  In other words, it must be one of ';
				msg += 'technology names already in the database.  If you are ';
				msg += 'unsure of valid names, press the up or down arrow keys ';
				msg += 'while this field has focus (has the blinking cursor), ';
				msg += 'and a list of options should appear.';
				errors['name'] = [msg];
			}
		} else {
			if ( ! tData.baseload )
				// necessary because we want the functionality of a radio button
				// but folks think in terms of a checkbox.  A radio button would
				// certaintly guarantee a defined .baseload, but would clutter the
				// UI with two buttons, when we only need a simple true/false.  In
				// other words, this is working with the semantics of a checkbox
				tData.baseload = false;
			if ( ! tData.storage )
				tData.storage = false;

			if ( tData.lifetime && (
			     isNaN(Number(tData.lifetime)) || ( Number(tData.lifetime) <= 0 )
			)) {
				var msg = 'Please specify a positive number or leave blank.';
				errors['lifetime'] = [msg];
			}

			if ( tData.loanlife && (
			     isNaN(Number(tData.loanlife)) || ( Number(tData.loanlife) <= 0 )
			)) {
				var msg = 'Please specify a positive number or leave blank.';
				errors['loanlife'] = [msg];
			}

			if ( tData.capacitytoactivity &&
			   isNaN(Number(tData.capacitytoactivity))
			) {
				var msg = 'Please specify a number or leave blank.';
				errors['capacitytoactivity'] = [msg];
			}

			// Capacity Factor
			var cfNewTS  = $.trim(cfData.CapacityFactorTechNew_timeslice)
			  , cfNewVal = $.trim(cfData.CapacityFactorTechNew_value);
			if ( cfNewTS.length || cfNewVal.length ) {
				if ( ! (cfNewTS.length && cfNewVal.length) ) {
					var msg = 'If you specify either field of a Capacity Factor, ';
					msg += 'you need to fill out both fields.  If you would rather ';
					msg += 'cancel, click anywhere outside of a field (so no ';
					msg += 'fields have focus), and push Shift to display the red ';
					msg += '"Cancel" button.';
					errors['General Error'] = [msg];
				}
				if ( isNaN(Number(cfNewVal)) ) {
					var msg = 'Please specify a number.';
					errors['CapacityFactorTechNew_value'] = [msg];
				}
				if ( ! cfNewTS.match( /^[A-z_]\w*, *[A-z_]\w*$/ ) ) {
					var msg = 'Invalid timeslice name.  If you are unsure of what ';
					msg += 'to put here, press the up or down arrow keys while ';
					msg += 'this field has focus (has the blinking cursor), and a ';
					msg += 'list of options should appear.';
					errors['CapacityFactorTechNew_timeslice'] = [msg];
				}
			}

			// Input Split
			var isNewInp = $.trim(isData.InputSplitNew_inp)
			  , isNewVal = $.trim(isData.InputSplitNew_value);
			if ( isNewInp.length || isNewVal.length ) {
				if ( ! (isNewInp.length && isNewVal.length) ) {
					var msg = 'If you specify either part of an Input Split, you ';
					msg += 'need to fill out both fields.  If you would rather ';
					msg += 'cancel, click anywhere outside of a field (so no ';
					msg += 'fields have focus), and push Shift to display the red ';
					msg += '"Cancel" button.';
					errors['General Error'] = [msg];
				}
				if ( isNaN(Number(isNewVal)) ) {
					var msg = 'Please specify a number.';
					errors['InputSplitNew_value'] = [msg];
				}
				if ( ! isNewInp.match( /^[A-z_]\w*$/ ) ) {
					var msg = 'Invalid commodity name.  If you are unsure of what ';
					msg += 'to put here, press the up or down arrow keys while ';
					msg += 'this field has focus (has the blinking cursor), and a ';
					msg += 'list of options should appear.';
					errors['InputSplitNew_inp'] = [msg];
				}
			}

			// Output Split
			var osNewInp = $.trim(osData.OutputSplitNew_out)
			  , osNewVal = $.trim(osData.OutputSplitNew_value);
			if ( osNewInp.length || osNewVal.length ) {
				if ( ! (osNewInp.length && osNewVal.length) ) {
					var msg = 'If you specify either part of an Output Split, you ';
					msg += 'need to fill out both fields.  If you would rather ';
					msg += 'cancel, click anywhere outside of a field (so no ';
					msg += 'fields have focus), and push Shift to display the red ';
					msg += '"Cancel" button.';
					errors['General Error'] = [msg];
				}
				if ( isNaN(Number(osNewVal)) ) {
					var msg = 'Please specify a number.';
					errors['OutputSplitNew_value'] = [msg];
				}
				if ( ! osNewInp.match( /^[A-z_]\w*$/ ) ) {
					var msg = 'Invalid commodity name.  If you are unsure of what ';
					msg += 'to put here, press the up or down arrow keys while ';
					msg += 'this field has focus (has the blinking cursor), and a ';
					msg += 'list of options should appear.';
					errors['OutputSplitNew_out'] = [msg];
				}
			}
		}

		if ( Object.keys( errors ).length > 0 ) {
			// client-side checking for user convenience.  The server will check
			// for itself, of course.
			Temoa.fn.enable( $inputs );
			Temoa.fn.displayErrors( $tTable, errors );
			return;
		}

		// client side error checking complete.
		to_save.push( [tech, tData] );

		for ( var name in cfData ) {
			var sel = '[name="' + name + '"]';
			if ( name.match(/^CapacityFactorTechNew/) ) {
				if ( name.match( /_timeslice$/ ) ) {
					var cf = $tTable.find( sel ).closest('tr').data('capacityfactor');
					to_save.push( [cf, {
					  timeslice: cfData.CapacityFactorTechNew_timeslice,
					  value:     cfData.CapacityFactorTechNew_value,
					}]);
				}
			} else if ( name.match(/^CapacityFactorTech_\d+$/) ) {
				var cf = $tTable.find( sel ).closest('tr').data('capacityfactor');
				to_save.push( [cf, {value: cfData[ name ]}] );
			}
		}

		for ( var name in isData ) {
			var sel = '[name="' + name + '"]';
			if ( name.match(/^InputSplitNew/) ) {
				if ( name.match( /_inp$/ ) ) {
					var is = $tTable.find( sel ).closest('tr').data('inputsplit');
					to_save.push( [is, {
					  inp:   isData.InputSplitNew_inp,
					  value: isData.InputSplitNew_value,
					}]);
				}
			} else if ( name.match(/^InputSplit_\d+$/) ) {
				var is = $tTable.find( sel ).closest('tr').data('inputsplit');
				to_save.push( [is, {value: isData[ name ]}] );
			}
		}

		for ( var name in osData ) {
			var sel = '[name="' + name + '"]';
			if ( name.match(/^OutputSplitNew/) ) {
				if ( name.match( /_out$/ ) ) {
					var os = $tTable.find( sel ).closest('tr').data('outputsplit');
					to_save.push( [os, {
					  out:   osData.OutputSplitNew_out,
					  value: osData.OutputSplitNew_value,
					}]);
				}
			} else if ( name.match(/^OutputSplit_\d+$/) ) {
				var os = $tTable.find( sel ).closest('tr').data('outputsplit');
				to_save.push( [os, {value: osData[ name ]}] );
			}
		}

		Temoa.fn.save_to_server({ to_save: to_save, inputs: $inputs, display: $tTable});
	},
	'[name="TechnologyCancel"] click': function ( $el, ev ) {  // AnalysisTechnologyDetail
		var $block = $el.closest('.technology');
		var t = $block.data('technology');

		// Because this is a Detail, there may be 2+ copies of it at a time.
		// They all will receive this click event, so put a guard in to only
		// continue if the event was meant for this technology.
		if ( t !== this.options.technology )
			return;

		// If this technology is new, the simplest way to cancel is just to
		// remove it.
		if ( t.isNew() ) {
			this.element.remove();
			return;
		}

		// Alright, now let's do the grunt work and reset various form values.
		// $block.find('[name="discountrate"]').val( p.attr('discountrate') || '' );

		// var cf = this.options.process.costsfixed;
		// if ( cf && cf.length && cf[0].isNew() ) cf[0].destroy();
	},
	'[name="TechnologyUpdate"] click': function ( $el, ev ) {  // AnalysisTechnologyDetail
		this.save( $el );
	},
	'[name="TechnologyCreate"] click': function ( $el, ev ) {  // AnalysisTechnologyDetail
		this.save( $el );
	},
	'input keyup': function ( $el, ev ) {  // AnalysisTechnologyDetail
		if ( 13 === ev.keyCode ) { // 13 == enter
			this.save( $(ev.target) );
		}
	},
	'[name="AddCapacityFactorTech"] click': function ( $el, ev ) {  // AnalysisTechnologyDetail
		var capfac_list = this.options.technology.capacityfactors;
		if ( capfac_list && capfac_list.length && capfac_list[0].isNew() ) {
			// only one new CF at a time.
			return;
		}

		var tOpts = this.options;
		var opts = { aId: tOpts.analysis.id, tId: tOpts.technology.id };

		// Create the client-side version, then display it.
		var newCF = new AnalysisTechnologyCapacityFactor( opts );
		capfac_list.unshift( newCF );
	},
	'[name="AddInputSplit"] click': function ( $el, ev ) {  // AnalysisTechnologyDetail
		var is_list = this.options.technology.inputsplits;
		if ( is_list && is_list.length && is_list[0].isNew() ) {
			// only one new split at a time.
			return;
		}

		var tOpts = this.options;
		var opts = { aId: tOpts.analysis.id, tId: tOpts.technology.id };
		var newIS = new AnalysisTechnologyInputSplit( opts );
		is_list.unshift( newIS );
	},
	'[name="AddOutputSplit"] click': function ( $el, ev ) { // AnalysisTechnologyDetail
		var os_list = this.options.technology.outputsplits;
		if ( os_list && os_list.length && os_list[0].isNew() ) {
			// only one new split at a time.
			return;
		}

		var tOpts = this.options;
		var opts = { aId: tOpts.analysis.id, tId: tOpts.technology.id };
		var newOS = new AnalysisTechnologyOutputSplit( opts );
		os_list.unshift( newOS );
	},
	'[name="CapacityFactorTechRemove"] click': function ( $el, ev ) { // AnalysisTechnologyDetail
		$el.closest( 'tr' ).data('capacityfactor').destroy();
	},
	'[name="InputSplitRemove"] click': function ( $el, ev ) { // AnalysisTechnologyDetail
		$el.closest( 'tr' ).data('inputsplit').destroy();
	},
	'[name="OutputSplitRemove"] click': function ( $el, ev ) { // AnalysisTechnologyDetail
		$el.closest( 'tr' ).data('outputsplit').destroy();
	},
	'{AnalysisTechnologyCapacityFactor} created' : function ( list, ev, obj ) {
		var segfracs = this.options.analysis.segfracs;
		for ( var i = 0; i < segfracs.length; ++i ) {
			if ( segfracs[ i ].id === obj.sfId )
				obj.attr('segfrac', segfracs[ i ] );
		}
	},
});


function BeginTemoaDBApp ( ) {

	function load_file ( url ) {
		// Handle failure as graceully as possible (if any), and tell user what
		// files failed to load.  They won't be able to do anything about it
		// directly, but it will be a debugging point for the TemoaUI devs.
		return $.cachedScript( url ).fail( function ( jqxhr, settings, exception ) {
			var msg = '<h1>Error loading required file: {file}</h1><p>Please accept our apologies.  There was an error loading a required file for TemoaUI.  Your browser says:</p><p style="background: #0ff;">{exception}</p><p>If a simple reload of this page does not correct this issue, please inform the Temoa Project.</p>';

			if ( url.indexOf('/') > -1 )
				url = url.slice(url.lastIndexOf('/') +1, url.length);

			msg = msg.replace('{file}', url );
			msg = msg.replace('{exception}', exception );
			$('body').empty().html( msg );
		});
	}

	var TemoaDBComponents = [
	  'TemoaDB_functions',
	  'TemoaDB_Models',
	  'TemoaDB_Views_AnalysisDetail',
	  'TemoaDB_Views_AnalysisList',
	  'TemoaDB_Views_AnalysisParameters',
	];
	var loaded = [];

	// Load all necessary components (hardcoded in this function), and proceed
	// only when finished.
	for ( var i = 0; i < TemoaDBComponents.length; ++i ) {
		var url = Temoa.C.base_js_url + TemoaDBComponents[ i ] + '.js';
		loaded[i] = load_file( url );
	}
	$.when.apply( null, loaded ).then( function ( ) {
		// All library elements have been loaded.  Begin the application!

	// The below complete: function has neither been setup, nor had a chance to
	// run at this point.  Given that some pieces of code rely on this cookie
	// for UI state info, we manually process the cookie the first time.
	Temoa.fn.processCookie();

	console.log( 'Begin TemoaDB' );
	Temoa.fn.showStatus( 'TemoaDB has begun.  Loading analyses ...', 'info' );

	$.ajaxSetup({
		crossDomain: false, //there should be no need to talk elsewhere
		complete: function( jqXHR, textStatus ) {
			Temoa.fn.processCookie( jqXHR );
			var status = jqXHR.status;
		},
		beforeSend: function ( xhr, settings ) {
			if ( ! Temoa.fn.csrfSafeMethod( settings.type )) {
				xhr.setRequestHeader( 'X-CSRFToken', $.cookie('csrftoken') );
			}
		},
		error: function ( jqXHR, textStatus, errorThrown ) {
			var status = jqXHR.status
			  , msg = null;
			if ( status >= 500 ) {
				if ( 501 === status ) {
					msg = "<p>501 (not implemented) - This message implies that you are testing new TemoaDB functionality, and that we have not implemented it yet.  If this is functionality you believe would be extremely helpful to your workflow, please let us know on the <a href='https://groups.google.com/forum/#!forum/temoa-project' title='GoogleGroups forum'>Temoa Project forum</a>.</p>";
				} else if ( 502 === status ) {
					msg = "<p>502 (bad gateway) - Some computer on the network that is between TemoaDB and your browser is having trouble communicating with us.  Hopefully this is a transient error, but if not, you may try connecting to TemoaDB from a different place.  Try contacting your local IT support for help, or accessing TemoaDB from a (different) coffee shop.</p>";
				} else if ( 503 === status ) {
					msg = "<p>503 (service unavailable) - The TemoaDB server is either offline for maintenance, or is overwhelmed by users.  Given the number of folks who know about TemoaDB, the former is most likely the issue.  If TemoaDB does not come back after a business day, consider inquiring on the <a href='https://groups.google.com/forum/#!forum/temoa-project' title='GoogleGroups forum'>Temoa Project forum</a>.</p>";
				} else if ( 504 === status ) {
					msg = "<p>504 (gateway timeout) - Some computer between TemoaDB and your browser did not receive a response from TemoaDB in a timely fashion.  This most likely means a temporary spike in traffic occurred: try again in a couple of minutes.</p>";
				} else if ( 505 === status ) {
					msg = "<p>505 (HTTP protocol not supported) - This message is extremely unlikely, so you may be using a non-standard browser.  Alternatively, your browser may have an incorrect setting, preventing it from using either HTTP v1 or v1.1.  Consider switching to a more mainstream browser (e.g. Chromium, Firefox, or Safari), or ask your local IT support for help.</p>";
				} else if ( 509 === status ) {
					msg = "<p>509 (bandwidth exceeded) - It appears that TemoaDB has gotten popular enough that this server has exceeded a bandwidth cap for this billing period.  If this error is not transient, please make sure we know about this via the <a href='https://groups.google.com/forum/#!forum/temoa-project' title='GoogleGroups forum'>Temoa Project forum</a>.</p>";
				} else if ( 511 === status ) {
					msg = "<p>511 (network authentication required) - This error most likely indicates a 'Captive Portal' situation: you may need to open a new browser tab or window and log on to a local network (e.g., agree to terms of service, pay money) before it will let you communicate with TemoaDB.</p>";
				} else if ( 522 === status ) {
					msg = "<p>522 (connection timed out) - TemoaDB's connection with your browser timed out.  This most likely means a lost couple of packets.  Resolution: try the action again.</p>";
				} else {
					msg = '<p>' + status + " - The server encountered a (currently undiagnosed) error.  If you can <strong>consistently</strong> recreate this error from a fresh reload (e.g., close and reopen the browser), then the Temoa Project developers would appreciate a bug report with the specifics.  Please file the bug on our <a href='https://github.com/hunteke/temoa/issues'>GitHub Issues</a> page.<p><p>Message from server: " + errorThrown + '</p>';
				}
			} else if ( status >= 400 ) {
				if ( 401 === status ) {
					msg = "<p>401 (unauthorized) - You are not currently known to the server.  This likely means that your session 'timed out' by not communicating with the server in an appropriate amount of time, or logged out in another tab or window (making this tab/window 'stale').  You will need to login again.";
				} else if ( 403 === status ) {
					msg = "<p>403 (forbidden) - Though the server recognizes you by the username '" + Temoa.fn.getCookie().username + "', the server does not recognize your authority to perform this action.  If you believe the action you took should be allowed (and thereby believe this message to be in error), please consider informing the Temoa Project via a <a href='https://github.com/hunteke/temoa/issues'>bug report.</a>  Note that unless you can provide exact instructions to recreate the issue, we may not be able to fix it.</p>"
				} else if ( 404 === status ) {
					msg = "<p>404 (not found) - The requested item could not be found.  Perhaps you need to reload the view in question?  If not, and you have discovered a <strong>recreatable</strong> error, please consider informing the Temoa Project via a <a href='https://github.com/hunteke/temoa/issues'>bug report.</a>  Note that unless there is an exact mechanism to recreate the issue, we may not be able to fix it.</p>";
				} else if ( 405 === status ) {
					msg = "<p>405 (method not allowed) - Your browser requested an action or resource through an incorrect mechanism.  This most likely indicates inconsitent logic in the Temoa web interface: if you can <em>consistently</em> recreate this message, please consider providing the Temoa Project with a <a href='https://github.com/hunteke/temoa/issues'>bug report.</a>  Note that unless there is an exact mechanism to recreate the issue, we may not be able to fix it.</p>";
				} else if ( 406 === status ) {
					msg = "<p>406 (not acceptable) - Your browser has told the server that it will only accept certain kinds of responses, none of which the server can produce.  This most likely indicates an incorrect setting or other issue with your browser.  You may ask for help on the <a href='https://groups.google.com/forum/#!forum/temoa-project' title='GoogleGroups forum'>Temoa Project forum</a>, but we will likely not be able to help.  Your local IT support may be of greater help.</p>";
				} else if ( 407 === status ) {
					msg = "<p>407 (unauthenticated proxy) - You are apparently accessing TemoaDB from through a proxy server.  This proxy server requires you to authenticate.  Generally, this means you will have to open a new tab or window and open a special organization-specific URL.  Your local IT support will be able to help as this error is not related to Temoa.</p>";
				} else if ( 408 === status ) {
					msg = "<p>408 (timeout) - The server was waiting for further information from your browser, but did not receive it in an appropriate amount of time.  This most likely means some packets were lost in transit (i.e., a fluke).  If you retry the action in question, it should succeed.</p>";
				} else if ( 410 === status ) {
					msg = "<p>410 (gone) - You or your browser requested some information from the server that no longer exists.  This likely means that you have an out-of-date version of the analysis.  If you reload this page (e.g., by closing and reopening your browser or force-reloading the page), this message should no longer appear.</p>";
				} else if ( 413 === status ) {
					msg = "<p>413 (too large) - You or your browser attempted to send too much data to the server.  As TemoaDB only deals with extremely small requests to the server (i.e., &lt;&lt; 512KiB), this is likely either an error with your browser or a bug within Temoa's web interface.  If you believe it to be the latter, please provide the Temoa Project with a <a href='https://github.com/hunteke/temoa/issues'>bug report.</a>  Note that unless there is an exact mechanism to recreate the issue, we may not be able to fix it.</p>";
				} else if ( 414 === status ) {
					msg = "<p>414 (request too long) - The request &ndash; what you would usually recognize as the URL in the white bar at the top of the browser window &ndash; for the request action was too long.  This request is not one that would see, but likely occurred when you selected a large number of items from a list.  Select a smaller number of items at a time to avoid this message.</p>";
				} else if ( 422 === status ) {
					return; // for form to handle
				} else if ( 429 === status ) {
					msg = "<p>429 (too many requests) - The server believes that you or your browser is asking for way too much information, and is therefore rate limiting your access.  To achieve this message, you would have to ask for an inordinate amount of information, such as what an automated program might be able to do.  This means you have scripted your access to TemoaDB (well done, but consider playing nice with our server), your browser has a bug, or you have found a bug within the Temoa web interface.  If you believe the latter, please consider creating a <a href='https://github.com/hunteke/temoa/issues'>bug report.</a>  Note that unless there is an exact mechanism to recreate the issue, we may not be able to fix it.</p>";
				} else {
					msg = '<p>' + status + " - There was a (currently undiagnosed) error with your browser's request to the server.  Consequently, the server has rejected the request.  If you can <strong>consistently</strong> recreate this error message from a fresh reload (e.g., close and reopen the browser), then the Temoa Project developers would appreciate a bug report with the specifics.  Please file the bug on our <a href='https://github.com/hunteke/temoa/issues'>GitHub Issues</a> page.<p><p>Message from server: " + errorThrown + '</p>';
				}
			}
			Temoa.fn.showStatus( null, null, msg );

		}
	});

	activeAnalysisList = new Analyses('#analysis_info');

	$(document).bind('keyup', 'shift+space', function () {
		var url = Temoa.C.ROOT_URL + '/static/process_interface/js/QuickFunction.js';
		url += '?_=' + new Date().getTime();
		$.getScript( url )
		.fail( function ( jqXHR, status, error ) {
			console.log(  'Error jqXHR: ', jqXHR );
			console.log(  'Error status message: ', status );
			console.log(  'Error information: ', error );
			Temoa.fn.showStatus('Error reading quick function.  Typo?');
		});
	});

	$(document).bind('keyup', 'ctrl+space', function () {
		var queryString = '?_=' + new Date().getTime();
		$('link[rel="stylesheet"]').each( function ( ) {
			this.href = this.href.replace(/\?.*|$/, queryString);
		});
	});
	$('#ShowHideAnalysis').click( function () {
		$('#analysis_detail').toggle( 'slide', {direction: 'up'} );
	});
	$('#ShowHideTechs').click( function () {
		$('#DBTechnologies').toggle( 'slide', {direction: 'down'} );
	});

	$(document).bind('keydown', 'shift', function ( e ) {
		Temoa.fn.hideStatus();
		Temoa.fn.showStatus('Enabling remove buttons ...', 'info');
		setTimeout( function ( ) { $('.remove').removeAttr('disabled'); }, 1 );
	});
	$(document).bind('keyup', 'shift', function ( e ) {
		Temoa.fn.hideStatus();
		Temoa.fn.showStatus('Disabling remove buttons ...', 'info');
		setTimeout( function ( ) { $('.remove').attr('disabled', true); }, 1 );
	});

	}); // all libraries loaded
}

$(document).ready( function () {
	var scripts = document.getElementsByTagName('script')
	  , this_script_url = scripts[scripts.length -1].src
	  , base_js_url = this_script_url.slice(0, this_script_url.lastIndexOf('/'));

	// As a special exception, define the base URL so that other JS scripts may
	// use it for loading.
	Temoa.C.base_js_url = base_js_url + '/';

	BeginTemoaDBApp();
});

})();

console.log( 'TemoaLib loaded: ' + Date() );
