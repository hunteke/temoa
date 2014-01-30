(function () {

"use strict";  // ECMA v5 pragma, similar to Perl's functionality.
  // FYI: http://ejohn.org/blog/ecmascript-5-strict-mode-json-and-more/

var COOKIE = 'TemoaDB_UISettings';

var DEBUG = window.location.search.indexOf( 'debug=true' ) > -1;
var ROOT_URL = window.location.pathname.replace( '/interact/', '' );

var activeAnalysisList   = null
  , activeTechnologyList = null
  , activeProcessList    = null
  ;

can.Model.prototype.clone = function ( ) {
	// Borrowed from: http://forum.javascriptmvc.com/topic/canjs-model-cloning
	var data = this.attr();
	delete data[ this.constructor.id ];
	return new this.constructor( data )
}

// Function borrowed from the Django Online documentation on CSRF:
// https://docs.djangoproject.com/en/dev/ref/contrib/csrf/
function csrfSafeMethod ( method ) {
	// these HTTP methods do not require CSRF protection
	return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}


function getCookie ( ) {
	var $obj = $.cookie( COOKIE );
	if ( $obj ) {
		return JSON.parse( atob( $obj ));
	}

	$obj = new Object();
	$obj.username    = null;
	$obj.analysis_id = null;
	$obj.process_ids = null;

	return $obj;
}

function setCookie ( obj ) {
	$.cookie( COOKIE, btoa( JSON.stringify( obj )));
}


function escapeHTML ( to_escape ) {
	var el = document.createElement('p');
	el.appendChild( document.createTextNode( to_escape ));
	return el.innerHTML;
};


function replaceNamedArgs ( str, replacements ) {
	for ( var i in replacements ) {
		var arg = '{' + i + '}';
		if ( str.indexOf( arg ) > -1 ) {
			str = str.replace( new RegExp( arg, 'g' ), replacements[i] );
		}
	}
	return str;
}


function disable ( list_of_inputs ) {
	for ( var i = 0; i < list_of_inputs.length; ++i ) {
		$(list_of_inputs[ i ]).attr('disabled', 'true');
	}
}

function enable ( list_of_inputs ) {
	for ( var i = 0; i < list_of_inputs.length; ++i ) {
		$(list_of_inputs[ i ]).removeAttr('disabled');
	}
}


function hideStatus ( nxt_func ) {
	var $status = $('#status');
	$status.empty();
	$status.clearQueue().stop(true, true).fadeOut( 1 );
	$status.addClass( 'hidden' );
	if ( nxt_func ) { nxt_func(); }
}


function showStatus ( msg, cssclass, safe_msg ) {
	var $st = $('<div>', {id: 'status'});
	if ( ! cssclass ) { cssclass = 'error' }

	if ( msg ) {
		msg = escapeHTML( msg );
	} else if ( safe_msg ) {
		msg = safe_msg;
	} else {
		return;
	}

	// From uncited "prior knowledge", I believe the average number of
	// characters per word in the English language is 5.1.  Similarly, I
	// believe that the average adult reads about 250 words per minute.
	// This suggests that the number of milliseconds before removing the status
	// message should be:
	//   numChars * (word/5.1 chars) * (min/250 words) * (60000ms/min)
	//    = numChars * (47.06 ms/char).  I round that to 50.
	var delayLength = 50 * msg.length;
	$st.addClass( cssclass );
	$st.html( msg );

	var actions = {
	  'error': function ( ) {
	    $st.clearQueue().stop(true, true).show().fadeIn( 1 ).delay(delayLength);
	    // flash twice
	    $st.fadeOut().fadeIn().delay( 1000 ).fadeOut().fadeIn();
	    $st.delay( 1000 ).fadeOut( 4000 ).queue( hideStatus );
	  },
	  'info' : function ( ) {
	    $st.clearQueue().stop(true, true).show().fadeIn( 1 ).delay( 1000 );
	    $st.fadeOut( 2000 ).queue( hideStatus );
	  }
	};
	actions[ cssclass ]();
	$('#status').replaceWith( $st );
}


function isInteger ( x ) {
	var _ceil = Math.ceil( Number(x) ), _floor = Math.floor( Number(x) );
	return (_ceil === _floor) && (_ceil === parseInt(x));
}


function displayErrors ( $el, errors ) {
	// errors should be a dictionary-like object of arrays.
	if ( 'General Error' in errors ) {
		$el.find('p.error').html( errors['General Error'] );
		delete errors['General Error'];
	}
	for ( var key in errors ) {
		var $input = $el.find('[name="' + key + '"]');
		var $err = $input.parent().find('.error');

		$input.focus(); // ideally only place at first input, but so what ...
		if ( ! $err.length ) {
			console.log( 'Warning: no errors displayed.  Element and Error ' +
			  'object: ', $el, errors );
		}
		for ( var i = 0; i < errors[key].length; ++i ) {
			$err.append( '<br />' + errors[key][i] );
		}
	}
}


function save_to_server ( args ) {
	// Will save a list of [model, data] tuples to the server, weeding out
	// information that has not changed.  Thus, this sends only the minimal
	// amount of data.  For example, if a user changes just one field, it is
	// the only field sent.

	// args is an object with three keys: to_save, inputs, display
	// args.to_save: Array of arrays of (model, new_data)
	//       [ [model1, data1], [model2, data2], ... ]
	// args.display is the jQuery wrapped element to be used for displaying
	//     server returned errors
	function send_data ( model_copy, data, $inputs, $displayContainer ) {
		var deferred = null;
		if ( model_copy.isNew() )
			deferred = model_copy.attr( data ).save();
		else
			// partialUpdate is what allows the minimal send, because save()
			// blithely sends everything.
			deferred = model_copy.partialUpdate( model_copy.id, data );

		deferred.then( function ( new_data, text_status, jqXHR ) {
			enable( $inputs );

			// "atomically" update model
			if ( model_copy.real_model.isNew() )
				model_copy.real_model.attr( new_data.attr() );
			else
				model_copy.real_model.attr( new_data );

			model_copy.real_model = null; // don't inadvertently remove real thing
			model_copy.attr({id: null}).destroy();

			showStatus('Saved!', 'info' );
		}, function ( jqXHR, text_status, description ) {
			enable( $inputs );
			model_copy.real_model = null; // don't inadvertently remove real thing
			model_copy.attr({id: null}).destroy();

			if ( jqXHR && jqXHR.responseJSON ) {
				displayErrors( $displayContainer, jqXHR.responseJSON );
			} else {
				console.log( 'Error received, but no JSON response: ', jqXHR );
				showStatus( 'Unknown error while saving data: ' + description );
			}
		});
	}

	// Data queued for saving, now check if anything has /actually/ changed, if
	// this was an accidental push of (for example) the enter key.
	var to_save = new Array();
	var check_for_save = args.to_save;
	for ( var i in check_for_save ) {
		var model = check_for_save[ i ][ 0 ];
		var data  = check_for_save[ i ][ 1 ];

		for ( var name in data ) {
			if ( ('' === data[ name ] && null == model[ name ])
				  || (data[ name ] == model[ name ] )
			) { // intentionally one triple equals; compares "1" and 1 equal
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

	if ( ! to_save.length ) {
		showStatus( 'No changes; no need to talk to server.', 'info' );
		enable( args.inputs );
		return;
	}

	for ( var i in to_save ) {
		var model = to_save[ i ][ 0 ];
		var data  = to_save[ i ][ 1 ];

		// Use a 'saver' object to simulate atomicity.  Only if there is
		// success do we update the model the UI is actually using. Meanwhile,
		// remove the id before destroying the saver object after we're done
		// with it so as not to remove the object in the database.
		var saver = new model.constructor( model.attr() );
		saver.real_model = model;
		send_data( saver, data, args.inputs, args.display );
	}
}

function numericSort ( lhs, rhs ) { return lhs - rhs; }

///////////////////////////////////////////////////////////////////////////////
//                        End miscellaneous functions                        //
///////////////////////////////////////////////////////////////////////////////

///////////////////////////////////////////////////////////////////////////////
//                            EJS helper functions                           //
///////////////////////////////////////////////////////////////////////////////

can.EJS.Helpers.prototype.escapeHTML = escapeHTML;

can.EJS.Helpers.prototype.apostrophe_escape = function ( s ) {
	return s.replace(/'/g, "&apos;");
}

can.EJS.Helpers.prototype.quote_escape = function ( s ) {
	return s.replace(/'/g, "&quot;");
}

///////////////////////////////////////////////////////////////////////////////
//                          End EJS helper functions                         //
///////////////////////////////////////////////////////////////////////////////

///////////////////////////////////////////////////////////////////////////////
//                               Event handlers                              //
///////////////////////////////////////////////////////////////////////////////

function update_timeslice ( mapping, oldKey ) {
	// Because the key is a timeslice name, and it is hardcoded by
	// the server, we need to update it if it changes.  Everything
	// would right itself if the user reloaded the page, but that
	// would get cumbersome.

	// Note that this operation requires it's own function so that
	// 'oldKey' is not bound via closure to an incorrect value.
	var timeslice = mapping.attr( oldKey ).attr('timeslice');
	timeslice.on('change',
		function ( ev, attr, how, newVal, oldVal ) {
		if ( 'set' !== how )
			return;

		var newName = timeslice.attr('name');
		var obj = mapping.attr( oldKey );
		mapping.attr( newName, obj );
		mapping.removeAttr( oldKey );
	});
}

///////////////////////////////////////////////////////////////////////////////
//                            End Event handlers                             //
///////////////////////////////////////////////////////////////////////////////

can.Model('AnalysisCommodity', {
	findOne: 'GET ' + ROOT_URL + '/analysis/{aId}/commodity/{id}',
	attributes: {
		aId: 'int',
		id:  'int',
		name: 'string',
	}
}, {});

AnalysisCommodity.extend('AnalysisCommodityDemand', {
	destroy: function ( id ) {
		var url = ROOT_URL;
		url += '/analysis/{aId}/delete/commodity/{id}';
		url = replaceNamedArgs( url, this.store[ id ].attr() );
		return $.ajax({ type: 'DELETE', url: url });
	},
	create:  'POST ' + ROOT_URL + '/analysis/{aId}/create/commodity/demand',
	update:  'POST ' + ROOT_URL + '/analysis/{aId}/update/commodity/{id}',
}, {
});
AnalysisCommodity.extend('AnalysisCommodityEmission', {
	destroy: function ( id ) {
		var url = ROOT_URL;
		url += '/analysis/{aId}/delete/commodity/{id}';
		url = replaceNamedArgs( url, this.store[ id ].attr() );
		return $.ajax({ type: 'DELETE', url: url });
	},
	create:  'POST ' + ROOT_URL + '/analysis/{aId}/create/commodity/emission',
	update:  'POST ' + ROOT_URL + '/analysis/{aId}/update/commodity/{id}',
}, {});
AnalysisCommodity.extend('AnalysisCommodityPhysical', {
	destroy: function ( id ) {
		var url = ROOT_URL;
		url += '/analysis/{aId}/delete/commodity/{id}';
		url = replaceNamedArgs( url, this.store[ id ].attr() );
		return $.ajax({ type: 'DELETE', url: url });
	},
	create:  'POST ' + ROOT_URL + '/analysis/{aId}/create/commodity/physical',
	update:  'POST ' + ROOT_URL + '/analysis/{aId}/update/commodity/{id}',
}, {});

can.Model('AnalysisCommodities', {
	findAll: 'GET ' + ROOT_URL + '/analysis/{aId}/commodity/list',
	attributes: {
		demand:   'AnalysisCommodityDemand.models',
		emission: 'AnalysisCommodityEmission.models',
		physical: 'AnalysisCommodityPhysical.models',
	}
}, {});

can.Model('AnalysisSegFrac', {
	create:  'POST '   + ROOT_URL + '/analysis/{aId}/segfrac/create',
	update:  'POST '   + ROOT_URL + '/analysis/{aId}/segfrac/update/{id}',
	destroy: 'DELETE ' + ROOT_URL + '/analysis/{aId}/segfrac/remove/{id}',
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
		var url = ROOT_URL;
		url += '/analysis/{aId}/segfrac/update/{id}';
		url = replaceNamedArgs( url, this.attr() );
		return $.post( url, attr );
	}
});

can.Model('AnalysisDemandDefaultDistribution', {
	create:  'POST '   + ROOT_URL + '/analysis/{aId}/demanddefaultdistribution/create/segfrac/{sfId}',
	update:  'POST '   + ROOT_URL + '/analysis/{aId}/demanddefaultdistribution/update/{id}',
	destroy: 'DELETE ' + ROOT_URL + '/analysis/{aId}/demanddefaultdistribution/remove/{id}',
	attributes: {
		aId: 'int',
		sfId: 'int',
		id: 'int',
		timeslice: 'AnalysisSegFrac.model',
		value: 'number'
	}
}, {
	partialUpdate: function ( id, attr ) {
		var url = ROOT_URL;
		url += '/analysis/{aId}/demanddefaultdistribution/update/{id}';
		url = replaceNamedArgs( url, this.attr() );
		return $.post( url, attr );
	}
});

can.Model('AnalysisDemandSpecificDistribution', {
	create:  'POST '   + ROOT_URL + '/analysis/{aId}/demandspecificdistribution/create/segfrac/{sfId}/demand/{dId}',
	update:  'POST '   + ROOT_URL + '/analysis/{aId}/demandspecificdistribution/update/{id}',
	destroy: 'DELETE ' + ROOT_URL + '/analysis/{aId}/demandspecificdistribution/remove/{id}',
	attributes: {
		aId: 'int',
		dId: 'int',
		sfId: 'int',
		id: 'int',
		timeslice: 'AnalysisSegFrac.model',
		value: 'number'
	}
}, {
	partialUpdate: function ( id, attr ) {
		var url = ROOT_URL;
		url += '/analysis/{aId}/demandspecificdistribution/update/{id}';
		url = replaceNamedArgs( url, this.attr() );
		return $.post( url, attr );
	}
});

can.Model('AnalysisDemand', {
	create:  'POST '   + ROOT_URL + '/analysis/{aId}/demand/create/commodity/{cId}/period/{period}',
	update:  'POST '   + ROOT_URL + '/analysis/{aId}/demand/update/{id}',
	destroy: 'DELETE ' + ROOT_URL + '/analysis/{aId}/demand/remove/{id}',
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
		var url = ROOT_URL;
		url += '/analysis/{aId}/demand/update/{id}';
		url = replaceNamedArgs( url, this.attr() );
		return $.post( url, attr );
	}
});

can.Model('Analysis', {
	findAll: 'GET ' + ROOT_URL + '/analysis/list',
	findOne: 'GET ' + ROOT_URL + '/analysis/view/{aId}',
	create:  function ( attrs ) {
		var url = ROOT_URL;
		url += '/analysis/create';
		return $.post( url, attrs, 'json' );
	},
	update:  function ( id, attrs ) {
		var url = ROOT_URL;
		url += '/analysis/{aId}/update';
		url = url.replace( /{aId}/, attrs.id );
		return $.post( url, attrs, 'json' );
	},
	destroy: 'DELETE ' + ROOT_URL + '/analysis/remove/{aId}',
	attributes: {
		id: 'int',
		username: 'string',
		name: 'string',
		description: 'string',
		global_discount_rate: 'number',
		vintages: 'string',
		period_0: 'int',
		segfracs: 'AnalysisSegFrac.models',

		// Comments left to show intended connection.  Problem: CanJS can't
		// return a /dictionary/ of Models, so instead dynamically create as a
		// Map of Maps, and convert each item to models during initialization.
		// (For implementation, search for 'ddd' below.)
//		demanddefaultdistribution: 'AnalysisDemandDefaultDistribution.models',
//		demandspecificdistribution: 'AnalysisDemandSpecificDistribution.models',
//		future_demands: 'AnalysisDemand.models',
		commodity_demand:   'AnalysisCommodityDemand.models',
		commodity_emission: 'AnalysisCommodityEmission.models',
		commodity_physical: 'AnalysisCommodityPhysical.models',
	}
}, {
	partialUpdate: function ( id, attr ) {
		var url = ROOT_URL;
		url += '/analysis/{aId}/update';
		url = replaceNamedArgs( url, this.attr() );
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
		var url = ROOT_URL;
		url += '/analysis/{id}/download_as_dat';
		url = replaceNamedArgs( url, this.attr() );
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
				return sum
		}

		return sum;
	}),
});

function clearAnalysisViews ( ) {
	$('#ProcessList .items').replaceWith(
		$('<div>', {class: 'items'}) );
	$('#AnalysisProcessDetails .items').replaceWith(
		$('<div>', {class: 'items'}) );
}


can.Control('Analyses', {
	defaults: {
			view: ROOT_URL + '/client_template/analysis_list.ejs'
		}
	},{
	init: function ( $el, options ) {
		var view = options.view;
		if ( DEBUG )
			view += '?_=' + new Date().getTime();

		var thisAnalyses = this;
		clearAnalysisViews()
		Analysis.findAll({}, function ( analyses ) {
			var username = getCookie().username || null;
			if ( username )
				analyses.unshift( new Analysis() );

			thisAnalyses.analyses = analyses
			var view_opts = {
				username: username,
				analyses: analyses
			}
			$el.html( can.view( view, view_opts ));
			$el.removeClass('hidden');

			var $cookie = getCookie();
			if ( $cookie.analysis_id ) {
				$('#analysis_selection').val( $cookie.analysis_id ).change();
			}

			showStatus('Analyses loaded.', 'info');
		}, function ( exception, data, status, xhr ) {
			if ( 'success' === status ) {
				console.log( exception );
				var msg = 'Potential programming error.  If you can recreate this ';
				msg += 'message after a page reload, please inform the ';
				msg += 'TemoaProject exactly how.  Library message: "';
				msg += exception.toString() + '"';
				showStatus( msg );
			} else {
				console.log( exception, data, status, xhr );
				showStatus( 'Unknown error retrieving analyses data.' );
			}
		});
	},
	'select change': function ( $el, event ) {
		clearAnalysisViews();
		var val = $el.val();
		var analysis;

		var $cookie = getCookie();
		$cookie.analysis_id = val;
		setCookie( $cookie );

		if ( ! val ) {
			$('#analysis_detail').fadeOut( function ( ) { $(this).empty(); });
			return;
		}

		analysis = $el.children('[value="' + val + '"]').data('analysis');
		var $div = $('<div>', {class: 'items'});
		$('#analysis_detail').fadeOut('fast', function ( ) {
			var $div = $('<div>', {id: 'analysis_detail'} );
			new AnalysisDetail( $div, {analysis: analysis} );
			$(this).replaceWith( $div );
		});

		if ( analysis.isNew() )
			return;

		new ProcessList( $div, {analysis: analysis} );
		$('#ProcessList').fadeIn();
		$('#ProcessList .items').replaceWith( $div );

	},
	'{Analysis} created' : function ( list, ev, analysis ) {
		this.analyses.unshift( new Analysis() );  // 'Create Analysis ...'
		$('#analysis_selection').val( analysis.id ).change();
	}
});

can.Control('AnalysisDetail', {
	defaults: {
			view: ROOT_URL + '/client_template/analysis_info.ejs'
		}
	},{
	init: function ( $el, options ) {
		var view = options.view;
		if ( DEBUG )
			view += '?_=' + new Date().getTime();

		var analysis = options.analysis;

		if ( ! analysis.commodity_emission )
			analysis.attr('commodity_emission',
			  new AnalysisCommodityEmission.List() );
		if ( ! analysis.commodity_demand )
			analysis.attr('commodity_demand',
			  new AnalysisCommodityDemand.List() );
		if ( ! analysis.commodity_physical )
			analysis.attr('commodity_physical',
			  new AnalysisCommodityPhysical.List() );
		if ( ! analysis.segfracs )
			analysis.attr('segfracs', new AnalysisSegFrac.List() );

		var view_opts = {
			username: getCookie().username || null,
			analysis: analysis,
		};

		$el.append( can.view( view, view_opts )).fadeIn();

		if ( analysis.isNew() )
			// a new analysis won't have anything attached to it ...
			return;

		AnalysisCommodities.findAll( {aId: analysis.id},
			function ( commodities ) {
				// Function declarations all at top to avoid confusion.  Hoisting
				// shouldn't be an issue; let's not inadvertently make it one.
				function delayed_add_to_map ( map, obj ) {
					// Obj is not yet finished building.  Harumph.  Exploit single-
					// threaded nature of browser, and use closure to update the map
					// after this thread has completed execution and the object is
					// finished building.
					setTimeout( function ( ) {
						map.attr( obj.name, obj );
					}, 1 ); // 1 = delay until after obj builds itself
				}
				function update_future_periods ( ev, attr, how, newVal, oldVal ) {
					var new_fp_list = analysis.vintages.split(',');
					var fp_list = analysis.future_periods;
					for ( var i = 0; i < new_fp_list.length; ++i )
						new_fp_list[ i ] = +new_fp_list[ i ];
					new_fp_list.sort( numericSort );

					fp_list.splice( 0 ); // remove all current elements
					for ( var i = 0; i < new_fp_list.length -1; ++i ) {
						// -1 == last year, which is _not_ a period
						if ( +new_fp_list[ i ] < analysis.period_0 )
							continue;
						fp_list.push( new_fp_list[i] );
					}
				}
				function update_future_demands ( ev, attr, how, newVal, oldVal ) {
					var fd_map   = analysis.future_demands;
					var fp_list  = analysis.future_periods.attr();
					var dem_list = analysis.commodity_demand.attr();
					var old_fd_map = fd_map.attr();

					for ( var i in fp_list ) {
						for ( var j in dem_list ) {
							var dem = dem_list[ j ];
							var key = dem.name + ', ' + fp_list[ i ];
							var fd = fd_map.attr( key );

							if ( ! fd ) {
								fd = new AnalysisDemand({
									aId:    analysis.id,
									cId:    dem.id,
									period: fp_list[ i ],
									commodity_name: dem.name
								});
							} else if ( ! fd.isNew ) {
								// CanJS doesn't convert non-List returned models, so we
								// need to explicitly make it a can.Model
								fd = new AnalysisDemand( fd.attr() );
							}
							fd_map.attr( key, fd );

							delete old_fd_map[ key ];
						}
					}

					for ( var key in old_fd_map )
						fd_map.removeAttr( key ); // clean up stale future demands
				}
				function update_outputs ( ev, attr, how, newVal, oldVal ) {
					var output_map = analysis.commodity_output;
					if ( 'remove' === how && typeof( oldVal ) === "object" ) {
						if ( oldVal.length && oldVal.length > 0 ) {
							for ( var i = 0; i < oldVal.length; ++i ) {
								output_map.removeAttr( oldVal[i].name );
							}
						}
					} else if ( 'add' === how && typeof( newVal ) === "object" ) {
						if ( newVal.length && newVal.length > 0 ) {
							for ( var i = 0; i < newVal.length; ++i ) {
								delayed_add_to_map( output_map, newVal[i] );
							}
						}
					}
				}

				// findAll returns a list, in this case of length 1
				var cp = commodities[0].physical;
				var cd = commodities[0].demand;
				var ce = commodities[0].emission;
				var c_output = new can.Map(); // to be union of cd & cp
				var future_periods = new can.List();
				var future_demands = analysis.future_demands || new can.Map();
				var segfracs = analysis.segfracs || new can.List();

				analysis.attr({
					commodity_emission: ce,
					commodity_demand:   cd,
					commodity_physical: cp,
					commodity_output:   c_output,  // to be union of cd & cp
					future_demands:     future_demands,
					future_periods:     future_periods,
					segfracs:           segfracs,
				});

				// set up commodity_output as union of demand and physical
				for ( var i = 0; i < cp.length; ++i )
					c_output.attr( cp[ i ].name, cp[ i ] );
				for ( var i = 0; i < cd.length; ++i )
					c_output.attr( cd[ i ].name, cd[ i ] );

				cp.on('change', update_outputs );
				cd.on('change', update_outputs );

				// important to bind to the specific attribute, rather than the
				// 'change' event.  Otherwise, the .push() will cause a 'change'
				// event that bubbles to the analysis model, initiating infinite
				// recursion.
				analysis.on('vintages', update_future_periods );
				analysis.on('vintages', update_future_demands );
				cd.on('change', update_future_demands );
				update_future_periods();
				update_future_demands();

				var _segFracs = {};
				var ddd_map = analysis.demanddefaultdistribution;
				var dsd_map = analysis.demandspecificdistribution;
				var dem_map = analysis.future_demands;

				for ( var i = 0; i < segfracs.length; ++i ) {
					var sf = segfracs[ i ];
					_segFracs[ sf.attr('name') ] = sf;
				}

				var dem_coms = analysis.commodity_demand;
				for ( var i = 0; i < analysis.commodity_demand.length; ++i ) {
					for ( var j = 0; j < future_periods.length; ++j ) {
						var cname = dem_coms[ i ]['name'];
						var dem_name = cname + ', ' + future_periods[ j ];
						var dem = future_demands.attr( dem_name )

						if ( ! dem ) {
							dem = new AnalysisDemand({
								aId: analysis.id,
								cId: dem_coms[ i ]['id'],
								period: future_periods[ i ],
								commodity_name: cname
							});
						} else if ( ! dem.isNew ) {
							// CanJS doesn't convert non-List returned models, so we
							// need to explicitly make it a can.Model
							dem = new AnalysisDemand( dem.attr() );
						}
						dem_map.attr( dem_name, dem );
					}
				}

				for ( var sf_key in _segFracs ) {
					var ddd = ddd_map[ sf_key ];
					var sf = _segFracs[ sf_key ];
					if ( ! ddd ) {
						ddd = new AnalysisDemandDefaultDistribution({
							aId: analysis.id,
							sfId: sf.attr('id')
						});
					} else if ( ! ddd.isNew ) {
						// Workaround a lacking feature in CanJS: there appears to
						// be no way to return a /dictionary/ of models via the
						// attributes plugin, only a can.List().  Unfortunately, we
						// only want random access for DDD.  So, we convert each
						// Map into a Model.
						ddd = new AnalysisDemandDefaultDistribution( ddd.attr() );
					}
					ddd.attr('timeslice', sf);
					ddd_map.attr( sf_key, ddd );
					update_timeslice( ddd_map, sf_key );
				}

				for ( var key in dsd_map.attr() ) {
					var dsd = dsd_map[ key ];
					var com_name = dsd[ 'name' ]
					var com = null;
					for ( var i = 0; i < analysis.commodity_demand.length; ++i ) {
						com = analysis.commodity_demand[ i ];
						if ( com[ 'name' ] === com_name ) {
							break;
						}
					}
					for ( var sf_key in _segFracs ) {
						var dist = dsd[ sf_key ];
						var sf = _segFracs[ sf_key ];
						if ( ! dist ) {
							dist = new AnalysisDemandSpecificDistribution({
								aId: analysis.id,
								dId: com['id'],
								sfId: sf['id'],
							});
						} else if ( ! dist.isNew ) {
							dist = new AnalysisDemandSpecificDistribution(
							  dist.attr() );
						}
						dist.attr( 'timeslice', sf );
						dsd.attr( sf_key, dist );
						update_timeslice( dsd, sf_key );
					}
				}

				new AnalysisCommodityLists( '#AnalysisCommodities', {
					analysis: analysis });

			}
		).fail( function ( error ) {
			console.log( error );
			showStatus( null, null, "Unknown error retrieving the Analysis' commodity list.  If you can recreate this error after <em>reloading</em> the page, please inform the Temoa Project developers.");
		});

		$el.find('#ShowHideCommodities').click( function ( ev ) {
			$('#AnalysisCommodities').toggle( 'slide', { direction: 'left' });
		});
		$el.find('#ShowHideAnalysisParameters').click( function ( ev ) {
			// due to the order of events when adding and removing various models
			// (e.g., commodity_demand items), it turns out to be necessary to
			// build this view afresh each time it is opened.  Or, more correctly,
			// to destroy it when it's closed.  Hence, the replaceWith call after
			// it's closed.
			var $div = $('#AnalysisParameters');

			if ( $div.is(':hidden') )
				// if it's currently hidden, the user has requested it be opened,
				// so, create it.
				new AnalysisParameters( '#AnalysisParameters', {
					analysis: analysis });

			$div.toggle( 'slide', { direction: 'left' }, function ( ) {
				// once closed, remove so control removes itself
				var $div = $(this);
				if ( $div.is(':hidden') )
					// this function is /after/ the effect has finished, so if it is
					// hidden now, then it's time to remove the control.  Replacing
					// the div with an empty new div also clears out things like
					// .data(), and event listeners, etc.
					$div.replaceWith($('<div>', {id: 'AnalysisParameters'}));
			});
		});
	},
	save: function ( $el ) {
		var errors = {};
		var $form = $el.closest('form');
		var inputs = $form.find(':input');
		var data = can.deparam( $form.serialize() );

		disable( inputs );
		$form.find('.error').empty();  // remove any previous errors

		// Vintages should be a comma separated list of vintages, which we test
		// by converting to an array.  However, it should remain a CSV.
		if ( ! data.vintages ) {
			var msg = 'Please specify at least 2 years, separated by commas.';
			errors['vintages'] = [msg];
		} else {
			var vs = data.vintages.split(/, */);
			if ( vs.length < 2 ) {
				var msg = 'Please specify at least 2 years, separated by commas.';
				errors['vintages'] = [msg];
			} else {
				for ( var i = 0; i < vs.length; ++i ) {
					var v = vs[ i ];
					if ( isNaN(Number(v)) || isNaN(parseInt(v)) ) {
						errors['vintages'] = ['"' + v + '" is not an integer.'];
						break;
					}
				}
			}
		}
		if ( ! data.name ) {
			var msg = 'Analysis needs a name!';
			errors['name'] = [msg];
		}
		if ( ! data.description || data.description.length < 5 ) {
			var msg = 'Please provide at least a minimal description.';
			errors['description'] = [msg];
		}
		if ( ! data.period_0 || ! isInteger( data.period_0 )) {
			var msg = 'Please specify an integer for Period 0.';
			errors['period_0'] = [msg];
		} else {
			var vs, period_0, is_valid = false;
			period_0 = parseInt( data.period_0 );
			vs = data.vintages.split(/, */);

			for ( var i = 0; i < vs.length; ++i ) vs[i] = +vs[i] // convert to num
				;

			if ( ! (vs.indexOf( period_0 ) > -1) ) {
				var msg = 'Period 0 must be one of the integers in vintages.';
				errors['period_0'] = [msg];
			} else if ( ! (period_0 < Math.max.apply(null, vs)) ) {
				var msg = 'Period 0 must be less than the largest value in ' +
				  'vintages.';
				errors['period_0'] = [msg];
			}
		}
		if ( ! data.global_discount_rate
		     || isNaN(Number(data.global_discount_rate)) ) {
			var msg = 'Please specify a global discount rate for this analysis.';
			errors['global_discount_rate'] = [msg];
		}

		if ( Object.keys( errors ).length > 0 ) {
			// client-side checking for user convenience.  The server will check
			// for itself, of course.
			enable( inputs );
			displayErrors( $form, errors );
			return;
		}

		var analysis = $el.closest('.analysis').data('analysis');
		var isNew = analysis.isNew();
		analysis.attr( data ).save( function ( model ) {
			enable( inputs );
			showStatus( 'Successfully saved.', 'info' );
		}, function ( xhr ) {
			enable( inputs );
			if ( xhr && xhr.responseJSON ) {
				displayErrors( $form, xhr.responseJSON );
			}
		});
	},
	'[name="AnalysisCreate"] click': function ( $el, ev ) {
		this.save( $el );
	},
	'[name="AnalysisUpdate"] click': function ( $el, ev ) {
		this.save( $el );
	},
	'[name="AnalysisCancel"] click': function ( $el, ev ) {
		var $item = $el.closest('.analysis');
		var analysis = $item.data('analysis');
		if ( analysis.isNew() ) {
			$('#analysis_selection').val( '' ).change();
			return;
		}

		$item.find('[name="name"]').val( analysis.name );
		$item.find('[name="description"]').val( analysis.description );
		$item.find('[name="global_discount_rate"]').val( analysis.global_discount_rate );
		$item.find('[name="vintages"]').val( analysis.vintages );
		$item.find('[name="period_0"]').val( analysis.period_0 );
		showStatus('Alteration cancelled', 'info');
	},
	'input keyup': function ( $el, ev ) {
		if ( 13 !== ev.keyCode )
			return;

		if ( ! $el.attr('form') )
			return;

		var $formAttr = $el.attr('form');
		if ( $el.attr('form').indexOf( 'AnalysisInfoForm_' ) === 0 ) {
			this.save( $el );
		}
	},
});


can.Control('AnalysisCommodityLists', {
	defaults: {
			view: ROOT_URL + '/client_template/analysis_commodities.ejs'
		}
	},{
	init: function ( $el, options ) {
		var view = options.view;
		if ( DEBUG )
			view += '?_=' + new Date().getTime();

		this.analysis = options.analysis;
		var analysis = this.analysis;  // needed for closure, below

		$el.html( can.view( view, {
			analysis: analysis,
			username: getCookie().username || null,
		}));

		$('#AnalysisCommoditiesCloseButton').click( function ( ) {
			$('#ShowHideCommodities').click();
		});

		var username = getCookie().username;
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
			var username = getCookie().username || null;

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

		disable( $inputs );
		$form.find('.error').empty();  // remove any previous errors

		if ( Object.keys( errors ).length > 0 ) {
			// client-side checking for user convenience.  The server will check
			// for itself, of course.
			enable( $inputs );
			displayErrors( $form, errors );
			return;
		}

		this.analysis.attr( data ).save(
			function ( model ) {
				enable( $inputs );
				showStatus( 'Analysis successfully created.', 'info' );
		}, function ( xhr ) {
				enable( $inputs );
				if ( xhr && xhr.responseJSON ) {
					displayErrors( $form, xhr.responseJSON );
				}
		});
	},
	createNewCommodity: function ( CommodityObj, commodityOpts ) {
		var $newDiv = $('<div>', {id: 'commodity_detail'} );
		new CommodityDetail( $newDiv, {
			username: getCookie().username || null,
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
			view: ROOT_URL + '/client_template/analysis_commodity_detail.ejs'
		}
	},{
	init: function ( $el, options ) {
		var view = options.view;
		if ( DEBUG )
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

		disable( inputs );
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
			enable( inputs );
			displayErrors( $form, errors );
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
				enable( inputs );
				model.attr( updated_model.attr() );  // "atomically" update

				saver.real_model = null;
				saver.attr( {id: null} ).destroy();  // don't delete in DB

				showStatus('Saved!', 'info' );
			}, function ( xhr ) {
				enable( inputs );
				saver.attr({id: null}).destroy();  // don't delete in DB

				if ( xhr && xhr.responseJSON ) {
					displayErrors( $form, xhr.responseJSON );
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

can.Control('AnalysisParameters', {
	defaults: {
			view: ROOT_URL + '/client_template/analysis_parameters.ejs'
		}
	},{
	init: function ( $el, options ) {
		var view = options.view;
		if ( DEBUG )
			view += '?_=' + new Date().getTime();

		this.analysis = this.options.analysis
		$el.html( can.view( view, {
			analysis: this.analysis,
			username: getCookie().username || null,
		}));
		$('#AnalysisParametersCloseButton').click( function ( ) {
			$('#ShowHideAnalysisParameters').click();
		});
	},
	'#AddTimeSlice click': function ( $el, ev ) {
		var segfracs = this.analysis.segfracs;
		if ( segfracs && segfracs.length > 0 && segfracs[0].isNew() )
			// only have one new time slice (segfrac) at a time
			return;

		segfracs.unshift( new AnalysisSegFrac({ aId: this.analysis.id }));
	},
	'#AddDemandDistribution click': function ( $el, ev ) {
		var com_demands = this.analysis.commodity_demand;
		var dsd_list = this.analysis.demandspecificdistribution;
		var $rows = $el.closest('table').find( 'tbody tr.dsd');

		if ( dsd_list !== null ) {
			if ( dsd_list.length === com_demands.length ) {
				var msg = 'All demands are already visible.';
				if ( ! dsd_list[ 0 ].attr('name') )
					msg = 'Please save new demand before adding another.';
				showStatus( msg, 'info' );

				return;
			} else if ( ! dsd_list[ 0 ].attr('name') ) {
				return; // only add one new DSD at a time.
			}
		} else {
			dsd_list = new can.List();
			this.analysis.demandspecificdistribution = dsd_list;
		}

		dsd_list.unshift( new can.Map());
	},
	saveSegFracs: function ( $el ) {  // AnalysisParameters
		var aId = this.analysis.id;
		var errors  = {};
		var to_save = new Array();
		var slice_name_id_re = /^SliceName_(\d*|New)$/;
		var slice_name_val_re = /^([A-z_]\w*),\s*([A-z_]\w*)$/
		var defaultdemand_id_re = /^DDD_(\d*)$/;

		var $sfForm = $( 'form#AnalysisSegFracs_' + aId );
		var $ddForm = $( 'form#AnalysisDemandDefaultDistribution_' + aId );
		var $sfTable = $el.closest('.segfracs');
		var $inputs = $sfTable.find(':input').not("[disabled='disabled']");
		var sfData  = can.deparam( $sfForm.serialize() );
		var ddData  = can.deparam( $ddForm.serialize() );

		$sfTable.find('.error').empty(); // remove any previous attempt's errors
		disable( $inputs );

		for ( var name in sfData ) {
			sfData[ name ] = $.trim( sfData[ name ]);
			if ( name.match( slice_name_id_re ) ) {
				if ( ! sfData[ name ]
				  || ! sfData[ name ].match( slice_name_val_re )
				) {
					var msg = 'The slice name must follow the form "[season, ';
					msg += 'time_of_day]", each beginning with a letter or ';
					msg += 'underscore, and only using alphanumeric characters.';
					errors[ name ] = [msg];
				}
			}

			if ( name.match( /^SliceValue_\d+$/ ) ) {
				if ( !   sfData[ name ]
					  || isNaN(Number( sfData[ name ]) )
					  || ! (0 < Number( sfData[ name ])
					         && Number( sfData[ name ] ) <= 1)
				) {
					var msg = 'Must be a number in the range (0, 1].';
					errors[ name ] = [msg];
				}
			}
		}

		for ( var name in ddData ) {
			ddData[ name ] = $.trim( ddData[ name ]);
			if ( name.match( defaultdemand_id_re ) ) {
				if ( ddData[ name ] === '' )
					continue;  // it /could/ be empty -- that's okay.
				if ( isNaN(Number( ddData[ name ]) )
					|| ! (0 < Number( ddData[ name ])
					       && Number( ddData[ name ] ) <= 1)
				) {
					var msg = 'Must be blank, or a number in the range (0, 1].';
					errors[ name ] = [msg];
				}
			}
		}

		if ( Object.keys( errors ).length > 0 ) {
			// client-side checking for user convenience.  The server will check
			// for itself, of course.
			enable( $inputs );
			displayErrors( $sfTable, errors );
			return;
		}

		for ( var name in sfData ) {
			var sel = '[name="' + name + '"]';
			var slice = $sfTable.find( sel ).closest('th').data('segfrac');

			if ( name.match( slice_name_id_re )) {
				var sfId = name.replace( slice_name_id_re, '$1' );
				var sf_season = sfData[ name ].replace( slice_name_val_re, '$1' );
				var sf_tod    = sfData[ name ].replace( slice_name_val_re, '$2' );
				to_save.push( [slice, {
				  season:      sf_season,
				  time_of_day: sf_tod,
				  value:       sfData[ 'SliceValue_' + sfId ],
				}]);
			}
		}

		for ( var name in ddData ) {
			var sel = '[name="' + name +'"]';
			var ddd = $sfTable.find( sel ).closest('td').data('slicedefault');
			if ( name.match( defaultdemand_id_re ) ) {
				to_save.push( [ddd, {value: ddData[ name ]}] )
			}
		}

		save_to_server({ to_save: to_save, inputs: $inputs, display: $sfTable });
	},
	saveDemands: function ( $el ) {  // AnalysisParameters
		console.log( 'Saving demands.');
		var aId = this.analysis.id;
		var errors  = {};
		var to_save = new Array();
		var to_remove = new Array();
		var demand_name_re = /^([A-z_]\w*), (\d+)$/;  // not flexible on space.

		var $form = $( 'form#AnalysisDemands_' + aId );
		var $demTable = $el.closest('.demands');
		var $inputs = $demTable.find(':input').not("[disabled='disabled']");
		var data = can.deparam( $form.serialize() );

		$demTable.find('.error').empty(); // remove any previous attempt's errors
		disable( $inputs );

		for ( var name in data ) {
			data[ name ] = $.trim( data[ name ]);
			if ( name.match( demand_name_re ) ) {
				if ( ! data[ name ] )
					continue;

				if ( isNaN(Number(data[ name ])) || 0 == Number(data[ name ]) ) {
					var msg = 'Must be empty, or a number in the range (0, 1].';
					errors[ name ] = [msg];
				}
			}
		}

		if ( Object.keys( errors ).length > 0 ) {
			// client-side checking for user convenience.  The server will check
			// for itself, of course.
			enable( $inputs );
			displayErrors( $demTable, errors );
			return;
		}

		for ( var name in data ) {
			console.log( 'data[' + name + '] = ', data[ name ] );

			if ( ! name.match( demand_name_re ) )
				continue;

			var sel = '[name="' + name + '"]';
			var $el = $demTable.find( sel ).closest('td');
			var dem = $el.data('demand');

			if ( ! data[ name ] && ! dem.isNew() ) {
				// if no value, and dem is not new, delete on server, and
				// replace locally.  This is in lieu of a button.
				to_remove.push( [dem, sel] );
				continue;
			}

			to_save.push( [dem, { value: data[ name ]}]);
		}

		for ( var i = 0; i < to_remove.length; ++i ) {
			var dem = to_remove[i][0];
			dem._sel = to_remove[i][1];
			console.log( 'REMOVE: ', to_remove[i]);

			dem.destroy( function ( destroyed_model ) {
				// Succeeded.  Now kill id and value locally.  Accordingly, there
				// is no need to create a new dem object.
				this.attr({id: null, value: null});

				var $el = $('.demands ' + this.sel);
				console.log( 'Animate? ', sel, $el );
				//this._el.animate({backgroundColor: '#dd0'
				//      }).animate({backgroundColor: 'transparent'});
				delete this.sel;
			}, function ( jqXHR, text_status, description ) {
				this._el.animate({backgroundColor: '#f00'
				      }).animate({backgroundColor: 'transparent'});
				this._el = null;
				delete this._el;

				if ( jqXHR && jqXHR.responseJSON ) {
					displayErrors( $dsdTable, jqXHR.responseJSON );
				} else {
					console.log( 'Error received, but no JSON response: ', jqXHR );
					showStatus( 'Unknown error while removing demand: '
					  + description );
				}
			});
		}

		save_to_server({ to_save: to_save, inputs: $inputs, display: $demTable });
	},
	saveDemandSpecificDistributions: function ( $el ) {  // AnalysisParameters
		var aId = this.analysis.id;
		var errors  = {};
		var to_save = new Array();
		var to_remove = new Array();
		var dsd_name_re = /^DSD_value_(\d+),(\d+)$/;

		var $form = $( 'form#AnalysisDemandSpecificDistribution_' + aId );
		var $dsdTable = $el.closest('.demandspecificdistributions');
		var $inputs = $dsdTable.find(':input').not("[disabled='disabled']");
		var data = can.deparam( $form.serialize() );

		console.log( 'DSD Data: ', data );

		$dsdTable.find('.error').empty(); // remove any previous attempt's errors
		disable( $inputs );

		if ( 'NewDSD_name' in data ) {
			var name = data.NewDSD_name;
			var dsd_list = analysis.demandspecificdistribution;
			var dem_list = analysis.commodity_demand;
			var valid_names = {};

			for ( var i = 0; i < dem_list.length; ++i )
				valid_names[ dem_list[i].name ] = true;
			if ( ! ( name in valid_names ))
				errors.NewDSD_name = ['Invalid demand commodity name.'];
			for ( var i = 0; i < dsd_list.length; ++i )
				if ( dsd_list[i]['name'] === name )
					errors.NewDSD_name = ['Already specified.'];
		}

		for ( var name in data ) {
			data[ name ] = $.trim( data[ name ]);
			if ( name.match( dsd_name_re ) ) {
				if ( ! data[ name ] )
					continue;

				if ( isNaN(Number(data[ name ])) || 0 === Number(data[ name ])) {
					var msg = 'Must be empty, or a number in the range (0, 1].';
					errors[ name ] = [msg];
				}
			}
		}

		if ( Object.keys( errors ).length > 0 ) {
			// client-side checking for user convenience.  The server will check
			// for itself, of course.
			enable( $inputs );
			displayErrors( $dsdTable, errors );
			return;
		}

		if ( 'NewDSD_name' in data ) {
			var dem_list = this.analysis.commodity_demand;
			var dsd_list = this.analysis.demandspecificdistribution;
			var dem_dists = dsd_list.shift();
			var dem = null;
			for ( var i = 0; i < dem_list.length; ++i ) {
				if ( dem_list[ i ].name === data.NewDSD_name ) {
					dem = dem_list[ i ];
					break;
				}
			}

			for ( var i = 0; i < analysis.segfracs.length; ++i ) {
				var sf = analysis.segfracs[ i ];
				var new_d = new AnalysisDemandSpecificDistribution({
					aId:  this.analysis.id,
					dId:  dem.id,
					sfId: sf.id,
					timeslice: sf,
				});
				dem_dists.attr( sf.attr('name'), new_d );
			}
			dem_dists.attr('name', dem.attr('name'));
			dsd_list.unshift( dem_dists );
		}

		for ( var name in data ) {
			if ( ! name.match( dsd_name_re ) )
				continue;

			var sel = '[name="' + name + '"]';
			var $el = $dsdTable.find( sel ).closest('td');
			var dsd = $el.data('demanddistribution');

			if ( ! data[ name ] && ! dsd.isNew() ) {
				// if no value, and dsd is not new, delete on server, and
				// replace locally.  This is in lieu of a button.
				to_remove.push( [$el, dsd] );
				continue;
			}

			to_save.push( [dsd, { value: data[ name ]}]);
		}

		for ( var i = 0; i < to_remove.length; ++i ) {
			var $el  = to_remove[i][0];
			var dsd  = to_remove[i][1];

			dsd._el = $el;
			dsd.destroy( function ( destroyed_model ) {
				// Succeeded.  Now kill id and value locally.  Note that there is
				// no need to create a new dsd object.
				this.attr({id: null, value: null});
				this._el.animate({backgroundColor: '#dd0'
				      }).animate({backgroundColor: 'transparent'});
				this._el = null;
				delete this._el;
			},
			function ( jqXHR, text_status, description ) {
				this._el.animate({backgroundColor: '#f00'
				      }).animate({backgroundColor: 'transparent'});
				this._el = null;
				delete this._el;

				if ( jqXHR && jqXHR.responseJSON ) {
					displayErrors( $dsdTable, jqXHR.responseJSON );
				} else {
					console.log( 'Error received, but no JSON response: ', jqXHR );
					showStatus( 'Unknown error while removing distribution: '
					  + description );
				}
			});
		}

		save_to_server({ to_save: to_save, inputs: $inputs, display: $dsdTable });
	},
	'[name="SegFracUpdate"] click': function ( $el, ev ) {
		this.saveSegFracs( $el );
	},
	'[name="DemandsUpdate"] click': function ( $el, ev ) {
		ev.preventBubble = true;
		this.saveDemands( $el );
		return false;
	},
	'[name="DemandSpecificDistributionsUpdate"] click': function ( $el, ev ) {
		this.saveDemandSpecificDistributions( $el );
	},
	'[name="SegFracRemove"] click': function ( $el, ev ) {
		$el.closest('th').data('segfrac').destroy();
	},
	'[name="DDDRemove"] click': function ( $el, ev ) {
		var ddd = $el.closest('td').data('slicedefault');
		var slice = ddd.timeslice;
		var slice_name = slice.name();
		ddd.destroy();

		ddd = new AnalysisDemandDefaultDistribution({
			aId: this.analysis.id,
			sfId: slice.id,
			timeslice: slice
		});
		this.analysis.demanddefaultdistribution.attr( slice_name, ddd );

		// Since the template keys off of segfracs, replacing the ddd is not
		// good enough.  Also, segfracs does not have a "setDirty" setter,
		// so we make it dirty with an effective non-op kludge:
		this.analysis.segfracs.unshift( this.analysis.segfracs.shift() );
	},
	'[name="SegFracCancel"] click': function ( $el, ev ) {
		var $item = $el.closest('.segfracs');
		var segfracs = this.analysis.segfracs;
		var demanddefaultdistribution = this.analysis.demanddefaultdistribution;

		if ( segfracs && segfracs.length > 0 && segfracs[0].isNew() )
			segfracs.shift();

		for ( var i = 0; i < segfracs.length; ++i ) {
			var sf = segfracs[ i ];
			var ddd = demanddefaultdistribution.attr( sf.attr('name') );
			ddd = ddd ? ddd.attr('value') : '';

			$item.find('[name="SliceName_' + sf.id + '"]').val( sf.attr('name') );
			$item.find('[name="SliceValue_' + sf.id + '"]').val( sf.value );
			$item.find('[name="DDD_' + sf.id + '"]').val( ddd );
		}

		$item.find('.error').empty();
		showStatus('Alteration cancelled', 'info');
	},
	'[name="DemandsCancel"] click': function ( $el, ev ) {
		var $item = $el.closest('.demands');
		var demands = this.analysis.commodity_demand;
		var future_demands = this.analysis.future_demands;

		for ( var key in future_demands.attr() ) {
			var val = future_demands.attr( key ).attr('value') || '';
			$item.find('[name="' + key + '"]').val( val );
		}

		$item.find('.error').empty();
		showStatus('Alteration cancelled', 'info');
	},
	'[name="DemandSpecificDistributionCancel"] click': function ( $el, ev ) {
		var $item = $el.closest('.demandspecificdistributions');
		var dsd_list = this.analysis.demandspecificdistribution;
		var segfrac_keys = {};

		if ( dsd_list )
			if ( ! dsd_list[0].attr('name') )
				// abort the adding of a new demand distribution set
				dsd_list.shift();

		for ( var i in dsd_list.attr() ) {
			var dem_dists = dsd_list.attr( i );
			for ( var j in dem_dists.attr() ) {
				var dsd = dem_dists[ j ];
				var name = 'DSD_value_' + dsd.dId + ',' + dsd.sfId;
				var val = dsd.value || '';

				$item.find('[name="' + name + '"]').val( val );
			}
		}

		$item.find('.error').empty();
		showStatus('Alteration cancelled', 'info');
	},
	'input keyup': function ( $el, ev ) {
		if ( ! $el.attr('form') )
			return;

		if ( 13 === ev.keyCode ) { // enter
			var formAttr = $el.attr('form');
			if ( 0 === formAttr.indexOf( 'AnalysisSegFracs_' )
			  || 0 === formAttr.indexOf( 'AnalysisDemandDefaultDistribution_' ))
			{
				this.saveSegFracs( $el );
			} else if ( 0 === formAttr.indexOf( 'AnalysisDemands_' )) {
				$('[name="DemandsUpdate"]').click();
			} else if ( 0 === formAttr.indexOf( 'AnalysisDemandSpecificDistribution_' )) {
				this.saveDemandSpecificDistributions( $el );
			}
		} else if ( 27 === ev.keyCode ) {  // escape
			var formAttr = $el.attr('form');

			if ( 0 === formAttr.indexOf( 'AnalysisSegFracs_' )
			  || 0 === formAttr.indexOf( 'AnalysisDemandDefaultDistribution_' ))
			{
				$el.closest('.segfracs').find('[name="SegFracCancel"]').click();
			}
			if ( 0 === formAttr.indexOf( 'AnalysisDemands_' )) {
				$el.closest('.demands').find('[name="DemandsCancel"]').click();
			}
			if ( 0 === formAttr.indexOf( 'AnalysisDemandSpecificDistribution_' )) {
				$el.closest('.demandspecificdistributions').find('[name="DemandSpecificDistributionCancel"]').click();
			}
		}
	},
	'{AnalysisSegFrac} created': function ( list, ev, segfrac ) {
		var slice_name = segfrac.name();
		var ddd = new AnalysisDemandDefaultDistribution({
			aId: this.analysis.id,
			sfId: segfrac.id,
		});
		this.analysis.demanddefaultdistribution.attr( slice_name, ddd );
	},
});

// ================== Technology MVC ==================
can.Model('Technology', {
	findAll: 'GET '    + ROOT_URL + '/technology/list',
	findOne: 'GET '    + ROOT_URL + '/technology/info/{tId}',
	create:  'POST '   + ROOT_URL + '/technology/create',
	update:  'POST '   + ROOT_URL + '/technology/update/{id}',
	destroy: 'DELETE ' + ROOT_URL + '/technology/remove/{id}',
	attributes: {
		id:   'int',
		username: 'string',
		name: 'string',
		capacity_to_activity: 'number',
		description: 'string'
	},
}, {});

can.Model('AnalysisTechnology', {
	findAll: 'GET '  + ROOT_URL + '/analysis/{aId}/technology/list',
	findOne: 'GET '  + ROOT_URL + '/analysis/{aId}/technology/info/{id}',
	update:  'POST ' + ROOT_URL + '/analysis/{aId}/technology/update/{id}',
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
		capacityfactors: 'AnalysisTechnologyCapacityFactor.models',
		inputsplits: 'AnalysisTechnologyInputSplit.models',
		outputsplits: 'AnalysisTechnologyOutputSplit.models',
	}
}, {
	partialUpdate: function ( id, attr ) {
		var url = ROOT_URL;
		url += '/analysis/{aId}/technology/update/{id}';
		url = replaceNamedArgs( url, this.attr() );
		return $.post( url, attr );
	}
});

can.Model('AnalysisTechnologyCapacityFactor', {
	create:  'POST ' + ROOT_URL + '/analysis/{aId}/technology/{tId}/CapacityFactor/create',
	update:  'POST ' + ROOT_URL + '/analysis/{aId}/technology/{tId}/CapacityFactor/update/{id}',
	destroy: function ( id ) {
		var url = ROOT_URL;
		url += '/analysis/{aId}/technology/{tId}/CapacityFactor/remove/{id}';
		url = replaceNamedArgs( url, this.store[ id ].attr() );
		return $.ajax({ type: 'DELETE', url: url });
	},
	attributes: {
		aId:     'int',
		tId:     'int',
		id:      'int',
		sfId:    'int',
		segfrac: 'AnalysisSegFrac.model',
		value:   'number',
	}
}, {
	partialUpdate: function ( id, attr ) {
		var url = ROOT_URL;
		url += '/analysis/{aId}/technology/{tId}/CapacityFactor/update/{id}';
		url = replaceNamedArgs( url, this.attr() );
		return $.post( url, attr );
	}
});

can.Model('AnalysisTechnologyInputSplit', {
	create:  'POST ' + ROOT_URL + '/analysis/{aId}/technology/{tId}/InputSplit/create',
	update:  'POST ' + ROOT_URL + '/analysis/{aId}/technology/{tId}/InputSplit/update/{id}',
	destroy: function ( id ) {
		var url = ROOT_URL;
		url += '/analysis/{aId}/technology/{tId}/InputSplit/remove/{id}';
		url = replaceNamedArgs( url, this.store[ id ].attr() );
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
		var url = ROOT_URL;
		url += '/analysis/{aId}/technology/{tId}/InputSplit/update/{id}';
		url = replaceNamedArgs( url, this.attr() );
		return $.post( url, attr );
	}
});

can.Model('AnalysisTechnologyOutputSplit', {
	findAll: 'GET ' + ROOT_URL + '/analysis/{aId}/technology/{tId}/OutputSplit/list',
	findOne: 'GET ' + ROOT_URL + '/analysis/{aId}/technology/{tId}/OutputSplit/{id}',
	create:  'POST ' + ROOT_URL + '/analysis/{aId}/technology/{tId}/OutputSplit/create',
	update:  'POST ' + ROOT_URL + '/analysis/{aId}/technology/{tId}/OutputSplit/update/{id}',
	destroy: function ( id ) {
		var url = ROOT_URL;
		url += '/analysis/{aId}/technology/{tId}/OutputSplit/remove/{id}';
		url = replaceNamedArgs( url, this.store[ id ].attr() );
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
		var url = ROOT_URL;
		url += '/analysis/{aId}/technology/{tId}/OutputSplit/update/{id}';
		url = replaceNamedArgs( url, this.attr() );
		return $.post( url, attr );
	}
});


can.Control('TechnologyCreate', {
	defaults: {
			view: ROOT_URL + '/client_template/technology_create.ejs'
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
			displayErrors( $form, errors );
			return;
		}

		var control = this;
		this.technology.attr( data ).save( function ( model ) {
			control.hide();
		}, function ( xhr ) {
			if ( xhr && xhr.responseJSON ) {
				displayErrors( $form, xhr.responseJSON );
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

can.Control('TechnologyList', {
	defaults: {
			view: ROOT_URL + '/client_template/technology_list.ejs'
		}
	},{
	init: function ( $el, options ) {
		var view = options.view;
		if ( DEBUG )
			view += '?_=' + new Date().getTime();

		Technology.findAll( {}, function ( technologies ) {
			activeTechnologyList = technologies;
			options['technologies'] = technologies;

			$el.empty()
			var view_opts = {
				username:  getCookie().username || null,
				technologies: technologies
			};

			$el.append( can.view( view, view_opts ));

			$('#DBTechnologiesCloseButton').click( function ( ) {
				$('#ShowHideTechs').click();
			});

			var $tbody = $el.find('.items:first tbody');

			$tbody.selectable( {} );
			$tbody.on( 'selectablestart', function () {
				$('#technology_info').fadeOut();
			});
			$tbody.on( 'selectablestop', function () {
				var $info = $('#technology_info');

				var $sel = $( this ).find( 'tr.ui-selected' );
				var techs = new Array();
				for ( var i = 0; i < $sel.length; ++i ) {
					techs.push( $($sel[i]).data().technology );
				}
				if ( ! (techs.length > 0) ) {
					return;
				}

				var $cookie = getCookie();
				var username = $cookie.username || null;

				function createTechnologyDetail ( toCreate ) {
					new TechnologyDetail( $info, {
						technology: toCreate.shift(),
						username: username
					});

					if ( toCreate.length > 0 ) {
						setTimeout( function () {
							createTechnologyDetail( toCreate );
						}, 50 );  // 50 = something tiny; i.e., "reluinquish thread"
					}
				}

				$info.fadeOut( 'fast', function ( ) {
					// these steps are crucial: the Detail Controls are bound to the
					// $info element, so it must be removed for GC.  We then recreate
					// it, and accordingly set the closure variable ($info)
					var $newInfo = $('<div>', {id: 'technology_info'} );
					$newInfo.css('display', 'none');
					$info.replaceWith( $newInfo );
					$info = $newInfo.fadeIn();

					createTechnologyDetail( techs );
				});
			});

			new TechnologyCreate('#technology_create', {
				technologies: technologies
			});
		});
	},
	'{Technology} created': function ( list, ev, technology ) {
		this.options.technologies.unshift( technology );
	},
	'[name="RemoveTechnology"] click': function ( $el, ev ) {
		$el.closest( 'tr' ).data('technology').destroy();
	}
});


can.Control('TechnologyDetail', {
	defaults: {
			view: ROOT_URL + '/client_template/technology_info.ejs'
		}
	},{
	init: function ( $el, options ) {
		var view = options.view;
		if ( DEBUG )
			view += '?_=' + new Date().getTime();

		var view_opts = {
			username: options.username,
			technology: options.technology
		};
		$el.append( can.view( view, view_opts ));
		$el = $el.children().last();  // after appending, only need the new el
		$el.css('display', 'none');
		$el.clearQueue().fadeIn();

		// must dynamically retrieve the actual element because it was not yet
		// created before this init() function.  this.element = ... does not work
		this.getElement = function ( ) { return $el.get(0); }
	},
	update: function ( $el ) {
		var errors = {};
		var $form = $el.closest('form');
		var data = can.deparam( $form.serialize() );
		$form.find('.error').empty();  // remove any old errors

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
			// client-side checking for user convenience.  The server will check
			// for itself, of course.
			displayErrors( $form, errors );
			return;
		}

		var control = this;
		var tech = $el.closest('.technology').data('technology');
		tech.attr( data ).save( function ( model ) {
			showStatus( 'Successfully updated.', 'info' );
		}, function ( xhr ) {
			if ( xhr && xhr.responseJSON ) {
				displayErrors( $form, xhr.responseJSON );
			}
		});
	},
	'[name="Update"] click': function ( $el, ev ) {
		if ( $(ev.target).closest('.technology').get(0) !== this.getElement() ) {
			return;
		}
		this.update( $el )
	},
	'[name="Cancel"] click': function ( $el, ev ) {
		if ( $(ev.target).closest('.technology').get(0) !== this.getElement() ) {
			return;
		}

		var $item = $( this.getElement() );
		var tech = $item.data('technology');
		$item.find('[name="description"]').val( tech.description );
		$item.find('[name="capacity_to_activity"]').val( tech.capacity_to_activity );
		showStatus('Alteration cancelled', 'info');
	},
	'input keyup': function ( $el, ev ) {
		if ( $(ev.target).closest('.technology').get(0) !== this.getElement() ) {
			return;
		}
		if ( 13 == ev.keyCode ) { // 13 = enter
			this.update( $el );
		}
	},
});

// ================== Process MVC ==================

can.Model('Process', {
	findAll: 'GET ' + ROOT_URL + '/analysis/{aId}/process/list/json',
	findOne: 'GET ' + ROOT_URL + '/analysis/{aId}/process/info/{id}',
	create:  'POST ' + ROOT_URL + '/analysis/{aId}/process/create',
	update:  'POST ' + ROOT_URL + '/analysis/{aId}/process/update/{id}',
	destroy: function ( id ) {
		var url = ROOT_URL;
		url += '/analysis/{aId}/process/remove/{id}';
		url = replaceNamedArgs( url, this.store[ id ].attr() );
		return $.ajax({ type: 'DELETE', url: url });
	},
	attributes: {
		id: 'int',
		aId: 'int',  // for updating, deleting (the urls)
		technology:         'AnalysisTechnology.model',
		costsfixed:         'ProcessCostFixed.models',
		costsvariable:      'ProcessCostVariable.models',
		efficiencies:       'ProcessEfficiency.models',
		emissionactivities: 'ProcessEmissionActivity.models',
	},
}, {
	partialUpdate: function ( id, attr ) {
		var url = ROOT_URL;
		url += '/analysis/{aId}/process/update/{id}';
		url = replaceNamedArgs( url, this.attr() );
		return $.post( url, attr );
	}
});

can.Model('ProcessCostFixed', {
	create:  'POST ' + ROOT_URL + '/analysis/{aId}/process/{pId}/create/CostFixed',
	update:  'POST ' + ROOT_URL + '/analysis/{aId}/process/{pId}/update/CostFixed/{id}',
	destroy: function ( id ) {
		var url = ROOT_URL;
		url += '/analysis/{aId}/process/{pId}/remove/CostFixed/{id}';
		url = replaceNamedArgs( url, this.store[ id ].attr() );
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
		var url = ROOT_URL;
		url += '/analysis/{aId}/process/{pId}/update/CostFixed/{id}';
		url = replaceNamedArgs( url, this.attr() );
		return $.post( url, attr );
	}
});

can.Model('ProcessCostVariable', {
	create:  'POST ' + ROOT_URL + '/analysis/{aId}/process/{pId}/create/CostVariable',
	update:  'POST ' + ROOT_URL + '/analysis/{aId}/process/{pId}/update/CostVariable/{id}',
	destroy: function ( id ) {
		var url = ROOT_URL;
		url += '/analysis/{aId}/process/{pId}/remove/CostVariable/{id}';
		url = replaceNamedArgs( url, this.store[ id ].attr() );
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
		var url = ROOT_URL;
		url += '/analysis/{aId}/process/{pId}/update/CostVariable/{id}';
		url = replaceNamedArgs( url, this.attr() );
		return $.post( url, attr );
	}
});

can.Model('ProcessEfficiency', {
	create:  'POST ' + ROOT_URL + '/analysis/{aId}/process/{pId}/create/Efficiency',
	update:  'POST ' + ROOT_URL + '/analysis/{aId}/process/{pId}/update/Efficiency/{id}',
	destroy: function ( id ) {
		var url = ROOT_URL;
		url += '/analysis/{aId}/process/{pId}/remove/Efficiency/{id}';
		url = replaceNamedArgs( url, this.store[ id ].attr() );
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
		var url = ROOT_URL;
		url += '/analysis/{aId}/process/{pId}/update/Efficiency/{id}';
		url = replaceNamedArgs( url, this.attr() );
		return $.post( url, attr );
	}
});

can.Model('ProcessEmissionActivity', {
	create:  'POST ' + ROOT_URL + '/analysis/{aId}/process/{pId}/create/EmissionActivity',
	update:  'POST ' + ROOT_URL + '/analysis/{aId}/Efficiency/{eId}/update/EmissionActivity/{id}',
	destroy: function ( id ) {
		var url = ROOT_URL;
		url += '/analysis/{aId}/Efficiency/{eId}/remove/EmissionActivity/{id}';
		url = replaceNamedArgs( url, this.store[ id ].attr() );
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
		var url = ROOT_URL;
		url += '/analysis/{aId}/Efficiency/{eId}/update/EmissionActivity/{id}';
		url = replaceNamedArgs( url, this.attr() );
		return $.post( url, attr );
	}
});



can.Control('ProcessList', {
	defaults: {
			view: ROOT_URL + '/client_template/process_list.ejs'
		}
	},{
	init: function ( $el, options ) {
		var view = options.view;
		if ( DEBUG )
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
			}

			var _segFracs = {};  // use as map
			for ( var i = 0; i < analysis.segfracs.length; ++i ) {
				var sf = analysis.segfracs[ i ];
				_segFracs[ sf.id ] = sf;
			}

			for ( var i = 0; i < technologies.length; ++i ) {
				var t = technologies[ i ];
				for ( var cfi = 0; cfi < t.capacityfactors.length; ++cfi ) {
					var cf = t.capacityfactors[ cfi ];
					cf.attr( 'segfrac', _segFracs[ cf.sfId ] );
				}
			}

			var view_opts = {
				username:  getCookie().username || null,
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

				ids.sort( numericSort );
				var $cookie = getCookie();
				$cookie.process_ids = ids;
				setCookie( $cookie );

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
						username: getCookie().username || null
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

			// Finally, pre-select what was selected in this session.
			// (Handy if the page needs to reload.)
			var $cookie = getCookie();
			if ( $cookie.process_ids ) {
				var ids = $cookie.process_ids;

				var sel = '[data-id="' + ids.join('"],[data-id="') + '"]';
				$tbody.find( sel ).addClass('ui-selected');
				$tbody.trigger('selectablestop')
			}
		}, function ( error ) {
			console.log( error );
			showStatus( 'An unknown error occurred while collecting analysis ' +
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
			username: getCookie().username || null,
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
				username: getCookie().username || null,
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
				username: getCookie().username || null,
				process: p,
				analysis: control.analysis
			});
			$( sel ).replaceWith( $div );
		}, 20 );
	},
	'{ProcessCostFixed} created': function ( list, ev, obj ) {
		var control = this;
		var new_cf  = obj.real_model;

		// The process template needs to be reprocessed.  Live binding is
		// currently only partially usable, working only if directly
		// attached to the DOM.  Wrapper code like '<% if ... %>' does not appear
		// to get reprocessed automatically.  So, replace the div in question.
		setTimeout( function ( ) {
			// necessary to do this work after a minor wait so that the new_ea
			// has a chance to update itself.  e.g., the pId would otherwise be
			// null.
			var pId  = new_cf.pId;
			var sel  = '#ProcessDetail_' + pId;
			var $div = $('<div>', {id: 'ProcessDetail_' + pId});
			var p    = $( sel ).find('.process').data('process');

			new ProcessDetail( $div, {
				username: getCookie().username || null,
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
			// necessary to do this work after a minor wait so that the new_ea
			// has a chance to update itself.  e.g., the pId would otherwise be
			// null.
			var pId  = new_cv.pId;
			var sel  = '#ProcessDetail_' + pId;
			var $div = $('<div>', {id: 'ProcessDetail_' + pId});
			var p    = $( sel ).find('.process').data('process');

			new ProcessDetail( $div, {
				username: getCookie().username || null,
				process: p,
				analysis: control.analysis
			});
			$( sel ).replaceWith( $div );
		}, 20 );
	},
});


can.Control('ProcessDetail', {
	defaults: {
			view: ROOT_URL + '/client_template/process_detail.ejs',
		}
	},{
	init: function ( $el, options ) {  // ProcessDetail
		var view = options.view;
		if ( DEBUG )
			view += '?_=' + new Date().getTime();

		var p = options.process;

		if ( ! p.costsfixed )
			p.attr('costsfixed', new ProcessCostFixed.List());
		if ( ! p.costsvariable )
			p.attr('costsvariable', new ProcessCostVariable.List());
		if ( ! p.efficiencies )
			p.attr('efficiencies', new ProcessEfficiency.List());
		if ( ! p.emissionactivities )
			p.attr('emissionactivities',
			  new ProcessEmissionActivity.List());

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
		  , $cfForm  = null, cfData  = null
		  , $cvForm  = null, cvData  = null
		  , $effForm = null, effData = null
		  , $emForm  = null, emData  = null
		  , check_for_save = new Array()
		  , to_save = new Array();
		var $pTable = $el.closest('.process');
		var $inputs = $pTable.find(':input');
		var process = $pTable.data('process');
		var pId = process.attr('id');

		if ( pId ) {
			// i.e., process already exists in DB
			$pForm   = $('#Process_' + pId);
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
		disable( $inputs );

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
			enable( $inputs );
			displayErrors( $pTable, errors );
			return;
		}

		// client side error checking complete.
		check_for_save.push( [process, pData] );

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

		save_to_server({ to_save: to_save, inputs: $inputs, display: $pTable });

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

		var cf = this.options.process.costsfixed;
		var cv = this.options.process.costsvariable;
		var e = this.options.process.efficiencies;
		var ea = this.options.process.emissionactivities;
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
			view: ROOT_URL + '/client_template/analysis_technology_detail.ejs',
		}
	},{
	init: function ( $el, options ) {  // AnalysisTechnologyDetail
		var view = options.view;
		if ( DEBUG )
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
		var $inputs = $tTable.find(':input');
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
		disable( $inputs );

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
			enable( $inputs );
			displayErrors( $tTable, errors );
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

		save_to_server({ to_save: to_save, inputs: $inputs, display: $tTable});
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
	}
});


function processCookie ( ) {
	// These settings are set by the server.  Changing them -- maliciously or
	// otherwise -- will only affect the client experience.  From a security
	// perspective, they have no bearing on the choices the server makes.

	var $ss = $.cookie( 'ServerState' );
	if ( ! $ss ) { return; }

	var $ss = JSON.parse( atob( $.cookie( 'ServerState' )));

	var $cookie = getCookie();
	if ( 'analysis_id'    in $ss ) {
		$cookie.analysis_id = $ss.analysis_id; }
	if ( 'process_ids'    in $ss ) {
		$cookie.process_ids = $ss.process_ids; }
	if ( 'technology_ids' in $ss ) {
		$cookie.technology_ids = $ss.technology_ids; }

	if ( 'username'      in $ss ) {
		var uname = $ss.username;
		$cookie.username = uname;
		if ( uname ) { $('#unauthorized').addClass('hidden'); }
		else         { $('#unauthorized').removeClass('hidden'); }
	}
	$.cookie( COOKIE, btoa( JSON.stringify( $cookie )));

	// To "prove" the above point, remove the cookie sent by the server,
	// although one cookie ($cookie) is as good as another ($ss).
	$.removeCookie( 'ServerState', { 'path' : '/' } );
}


function BeginTemoaDBApp ( ) {
	// The below complete: function has neither been setup, nor had a chance to
	// run at this point.  Given that some pieces of code rely on this cookie
	// for UI state info, we manually process the cookie the first time.
	processCookie();

	console.log( 'Begin TemoaDB' );
	showStatus( 'TemoaDB has begun.  Loading analyses ...', 'info' );

	$.ajaxSetup({
		crossDomain: false, //there should be no need to talk elsewhere
		complete: function( jqXHR, textStatus ) {
			processCookie( jqXHR );
			var status = jqXHR.status;
		},
		beforeSend: function ( xhr, settings ) {
			if ( ! csrfSafeMethod( settings.type )) {
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
					msg = "<p>403 (forbidden) - Though the server recognizes you by the username '" + getCookie().username + "', the server does not recognize your authority to perform this action.  If you believe the action you took should be allowed (and thereby believe this message to be in error), please consider informing the Temoa Project via a <a href='https://github.com/hunteke/temoa/issues'>bug report.</a>  Note that unless you can provide exact instructions to recreate the issue, we may not be able to fix it.</p>"
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
			showStatus( null, null, msg );

		}
	});

	new TechnologyList('#technology_list');
	activeAnalysisList = new Analyses('#analysis_info');

	$('#QuickFunction').click( function () {
		var url = ROOT_URL + '/static/process_interface/js/QuickFunction.js';
		url += '?_=' + new Date().getTime();
		$.getScript( url )
		.fail( function ( jqXHR, status, error ) {
			console.log(  'Error jqXHR: ', jqXHR );
			console.log(  'Error status message: ', status );
			console.log(  'Error information: ', error );
			showStatus('Error reading quick function.  Typo?');
		});
	});
	$(document).bind('keyup', 'shift+space', function ( ) {
		$('#QuickFunction').trigger('click');
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
		hideStatus();
		showStatus('Enabling remove buttons ...', 'info');
		setTimeout( function ( ) { $('.remove').removeAttr('disabled'); }, 1 );
	});
	$(document).bind('keyup', 'shift', function ( e ) {
		hideStatus();
		showStatus('Disabling remove buttons ...', 'info');
		setTimeout( function ( ) { $('.remove').attr('disabled', true); }, 1 );
	});
}

$(document).ready( function () {
	if ( DEBUG )
		$.getScript( ROOT_URL + '/static/process_interface/js/ejs_fulljslint.js' );

	BeginTemoaDBApp();
});

})();

console.log( 'TemoaLib loaded: ' + Date() );

