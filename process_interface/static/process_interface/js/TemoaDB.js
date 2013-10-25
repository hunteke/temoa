"use strict";  // ECMA v5 pragma, similar to Perl's functionality.
  // FYI: http://ejohn.org/blog/ecmascript-5-strict-mode-json-and-more/

(function () {
var COOKIE = 'TemoaDB_UISettings';

var DEBUG = window.location.search.indexOf( 'debug=true' ) > -1;

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
		return JSON.parse( $obj );
	}

	$obj = jQuery( new Object() );
	$obj.username    = null;
	$obj.analysis_id = null;
	$obj.process_ids = null;

	return $obj;
}

function setCookie ( obj ) {
	$.cookie( COOKIE, JSON.stringify( obj ));
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
		var $err = $el.find('[name="' + key + '"]').parent().find('.error');
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
	// amount of data.  For example, if a user changes just one field, the only
	// that field is sent.

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
			if ( ('' === data[ name ] && null === model[ name ])
				  || (data[ name ] == model[ name ] )
			) { // intentional double equals; compares "1" and 1 equal
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

can.Model('AnalysisCommodity', {
	findOne: 'GET /analysis/{aId}/commodity/{id}',
	attributes: {
		aId: 'int',
		id:  'int',
		name: 'string',
	}
}, {});

AnalysisCommodity.extend('AnalysisCommodityDemand', {
	destroy: function ( id ) {
		var url = '/analysis/{aId}/delete/commodity/{id}';
		url = replaceNamedArgs( url, this.store[ id ].attr() );
		return $.ajax({ type: 'DELETE', url: url });
	},
	create:  'POST /analysis/{aId}/create/commodity/demand',
	update:  'POST /analysis/{aId}/update/commodity/{id}',
}, {
});
AnalysisCommodity.extend('AnalysisCommodityEmission', {
	destroy: function ( id ) {
		var url = '/analysis/{aId}/delete/commodity/{id}';
		url = replaceNamedArgs( url, this.store[ id ].attr() );
		return $.ajax({ type: 'DELETE', url: url });
	},
	create:  'POST /analysis/{aId}/create/commodity/emission',
	update:  'POST /analysis/{aId}/update/commodity/{id}',
}, {});
AnalysisCommodity.extend('AnalysisCommodityPhysical', {
	destroy: function ( id ) {
		var url = '/analysis/{aId}/delete/commodity/{id}';
		url = replaceNamedArgs( url, this.store[ id ].attr() );
		return $.ajax({ type: 'DELETE', url: url });
	},
	create:  'POST /analysis/{aId}/create/commodity/physical',
	update:  'POST /analysis/{aId}/update/commodity/{id}',
}, {});

can.Model('AnalysisCommodities', {
	findAll: 'GET /analysis/{aId}/commodity/list',
	attributes: {
		demand:   'AnalysisCommodityDemand.models',
		emission: 'AnalysisCommodityEmission.models',
		physical: 'AnalysisCommodityPhysical.models',
	}
}, {});


can.Model('Analysis', {
	findAll: 'GET /analysis/list',
	findOne: 'GET /analysis/view/{aId}',
	//create:  'POST /analysis/create',
	create:  function ( attrs ) {
		return $.post( '/analysis/create', attrs, 'json' );
	},
	update:  function ( id, attrs ) {
		var url = '/analysis/{aId}/update';
		url = url.replace( /{aId}/, attrs.id );
		return $.post( url, attrs, 'json' );
	},
	destroy: 'DELETE /analysis/remove/{aId}',
	attributes: {
		id: 'int',
		username: 'string',
		name: 'string',
		description: 'string',
		global_discount_rate: 'number',
		vintages: 'string',
		period_0: 'int',
		commodity_demand:   'AnalysisCommodityDemand.models',
		commodity_emission: 'AnalysisCommidityEmission.models',
		commodity_physical: 'AnalysisCommodityPhysical.models',
	}
}, {});

function clearAnalysisViews ( ) {
	$('#ProcessList .items').replaceWith(
		$('<div>', {class: 'items'}) );
	$('#AnalysisProcessDetails .items').replaceWith(
		$('<div>', {class: 'items'}) );
}


can.Control('Analyses', {
	defaults: {
			view: '/static/process_interface/templates/analysis_list.ejs'
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
			view: '/static/process_interface/templates/analysis_info.ejs'
		}
	},{
	init: function ( $el, options ) {
		var view = options.view;
		if ( DEBUG )
			view += '?_=' + new Date().getTime();

		var analysis = options.analysis;
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
				function _add_to_observe ( observer, obj ) {
					setTimeout( function ( ) {
						observer.attr( obj.name, obj );
					}, 1 ); // 1 = delay until after obj builds itself
				}

				// findAll returns a list, in this case of length 1
				var coms = commodities[0];
				var cp = coms.physical;
				var cd = coms.demand;
				analysis.attr( 'commodity_emission', coms.emission );
				analysis.attr( 'commodity_demand', cd );
				analysis.attr( 'commodity_physical', cp );

				var output = new can.Observe();
				analysis.attr('commodity_output', output);
				for ( var i = 0; i < cp.length; ++i )
					output.attr( cp[ i ].name, cp[ i ] );
				for ( var i = 0; i < cd.length; ++i )
					output.attr( cd[ i ].name, cd[ i ] );

				function output_change ( ev, attr, how, newVal, oldVal ) {
					if ( 'remove' === how && typeof( oldVal ) === "object" ) {
						if ( oldVal.length && oldVal.length > 0 ) {
							for ( var i = 0; i < oldVal.length; ++i ) {
								output.removeAttr( oldVal[i].name );
							}
						}
					} else if ( 'add' === how && typeof( newVal ) === "object" ) {
						if ( newVal.length && newVal.length > 0 ) {
							for ( var i = 0; i < newVal.length; ++i ) {
								_add_to_observe( output, newVal[i] );
							}
						}
					}
				}
				cp.bind('change', output_change );
				cd.bind('change', output_change );

				new AnalysisCommodityLists( '#AnalysisCommodities', {
					analysis: analysis });
			}
		).fail( function ( error ) {
			console.log( error );
			showStatus( null, null, "Unknown error retrieving the Analysis' commodity list.  If you can recreate this error after <em>reloading</em> the page, please inform the Temoa Project developers.");
		});

		$el.find('#ShowHideCommodities').click( function ( ev ) {
			$('#AnalysisCommodities').toggle( 'slide', {
				direction: 'left'
			});
		});
	},
	save: function ( $el ) {
		var errors = {};
		var $form = $el.closest('form');
		var inputs = $form.find('input,textarea');
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
			displayErrors( $form, errors );
			enable( inputs );
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
		if ( $el.attr('form') && $el.attr('form').indexOf( 'Analysis' ) === 0 ) {
			if ( 13 === ev.keyCode ) {
				this.save( $el );
			}
		}
	},
});


can.Control('AnalysisCommodityLists', {
	defaults: {
			view: '/static/process_interface/templates/analysis_commodities.ejs'
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
		var $inputs = $form.find('input,textarea');
		var data   = can.deparam( $form.serialize() );

		disable( $inputs );
		$form.find('.error').empty();  // remove any previous errors

		if ( Object.keys( errors ).length > 0 ) {
			// client-side checking for user convenience.  The server will check
			// for itself, of course.
			displayErrors( $form, errors );
			enable( $inputs );
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
			view: '/static/process_interface/templates/analysis_commodity_detail.ejs'
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
		var errors  = {};
		var $form   = $el.closest( 'form' );
		var inputs = $form.find('input,textarea');
		var data    = can.deparam( $form.serialize() );

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
			displayErrors( $form, errors );
			enable( inputs );
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


// ================== Technology MVC ==================
can.Model('Technology', {
	findAll: 'GET /technology/list',
	findOne: 'GET /technology/info/{tId}',
	create:  'POST /technology/create',
	update:  'POST /technology/update/{id}',
	destroy: 'DELETE /technology/remove/{id}',
	attributes: {
		id:   'int',
		username: 'string',
		name: 'string',
		capacity_to_activity: 'number',
		description: 'string'
	},
}, {});

can.Model('AnalysisTechnology', {
	findAll: 'GET /analysis/{aId}/technology/list',
	findOne: 'GET /analysis/{aId}/technology/info/{id}',
	update:  'POST /analysis/{aId}/technology/update/{id}',
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
		inputsplits: 'AnalysisTechnologyInputSplit.models',
		outputsplits: 'AnalysisTechnologyOutputSplit.models',
	}
}, {
	partialUpdate: function ( id, attr ) {
		var url = '/analysis/{aId}/technology/update/{id}';
		url = replaceNamedArgs( url, this.attr() );
		return $.post( url, attr );
	}
});

can.Model('AnalysisTechnologyInputSplit', {
	create:  'POST /analysis/{aId}/technology/{tId}/InputSplit/create',
	update:  'POST /analysis/{aId}/technology/{tId}/InputSplit/update/{id}',
	destroy: function ( id ) {
		var url = '/analysis/{aId}/technology/{tId}/InputSplit/remove/{id}';
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
		var url = '/analysis/{aId}/technology/{tId}/InputSplit/update/{id}';
		url = replaceNamedArgs( url, this.attr() );
		return $.post( url, attr );
	}
});

can.Model('AnalysisTechnologyOutputSplit', {
	findAll: 'GET /analysis/{aId}/technology/{tId}/OutputSplit/list',
	findOne: 'GET /analysis/{aId}/technology/{tId}/OutputSplit/{id}',
	create:  'POST /analysis/{aId}/technology/{tId}/OutputSplit/create',
	update:  'POST /analysis/{aId}/technology/{tId}/OutputSplit/update/{id}',
	destroy: function ( id ) {
		var url = '/analysis/{aId}/technology/{tId}/OutputSplit/remove/{id}';
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
		var url = '/analysis/{aId}/technology/{tId}/OutputSplit/update/{id}';
		url = replaceNamedArgs( url, this.attr() );
		return $.post( url, attr );
	}
});


can.Control('TechnologyCreate', {
	defaults: {
			view: '/static/process_interface/templates/technology_create.ejs'
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
			view: '/static/process_interface/templates/technology_list.ejs'
		}
	},{
	init: function ( $el, options ) {
		var view = options.view;
		if ( DEBUG )
			view += '?_=' + new Date().getTime();

		Technology.findAll( {}, function ( technologies ) {
			activeTechnologyList = technologies;
			options['technologies'] = technologies;

			$el.empty().fadeOut();
			var view_opts = {
				username:  getCookie().username || null,
				technologies: technologies
			};

			$el.append( can.view( view, view_opts ));
			$el.fadeIn();

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
			view: '/static/process_interface/templates/technology_info.ejs'
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
	findAll: 'GET /analysis/{aId}/process/list/json',
	findOne: 'GET /analysis/{aId}/process/info/{id}',
	create:  'POST /analysis/{aId}/process/create',
	update:  'POST /analysis/{aId}/process/update/{id}',
	destroy: function ( id ) {
		var url = '/analysis/{aId}/process/remove/{id}';
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
		var url = '/analysis/{aId}/process/update/{id}';
		url = replaceNamedArgs( url, this.attr() );
		return $.post( url, attr );
	}
});

can.Model('ProcessCostFixed', {
	create:  'POST /analysis/{aId}/process/{pId}/create/CostFixed',
	update:  'POST /analysis/{aId}/process/{pId}/update/CostFixed/{id}',
	destroy: function ( id ) {
		var url = '/analysis/{aId}/process/{pId}/remove/CostFixed/{id}';
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
		var url = '/analysis/{aId}/process/{pId}/update/CostFixed/{id}';
		url = replaceNamedArgs( url, this.attr() );
		return $.post( url, attr );
	}
});

can.Model('ProcessCostVariable', {
	create:  'POST /analysis/{aId}/process/{pId}/create/CostVariable',
	update:  'POST /analysis/{aId}/process/{pId}/update/CostVariable/{id}',
	destroy: function ( id ) {
		var url = '/analysis/{aId}/process/{pId}/remove/CostVariable/{id}';
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
		var url = '/analysis/{aId}/process/{pId}/update/CostVariable/{id}';
		url = replaceNamedArgs( url, this.attr() );
		return $.post( url, attr );
	}
});

can.Model('ProcessEfficiency', {
	create:  'POST /analysis/{aId}/process/{pId}/create/Efficiency',
	update:  'POST /analysis/{aId}/process/{pId}/update/Efficiency/{id}',
	destroy: function ( id ) {
		var url = '/analysis/{aId}/process/{pId}/remove/Efficiency/{id}';
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
		var url = '/analysis/{aId}/process/{pId}/update/Efficiency/{id}';
		url = replaceNamedArgs( url, this.attr() );
		return $.post( url, attr );
	}
});

can.Model('ProcessEmissionActivity', {
	create:  'POST /analysis/{aId}/process/{pId}/create/EmissionActivity',
	update:  'POST /analysis/{aId}/Efficiency/{eId}/update/EmissionActivity/{id}',
	destroy: function ( id ) {
		var url = '/analysis/{aId}/Efficiency/{eId}/remove/EmissionActivity/{id}';
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
		var url = '/analysis/{aId}/Efficiency/{eId}/update/EmissionActivity/{id}';
		url = replaceNamedArgs( url, this.attr() );
		return $.post( url, attr );
	}
});



can.Control('ProcessList', {
	defaults: {
			view: '/static/process_interface/templates/process_list.ejs'
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
			control.technologies = new can.Observe();
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
			var view_opts = {
				username:  getCookie().username || null,
				analysis:  analysis,
				processes: processes
			};

			// set up the autocomplete name options for new Process()es
			var new_process_names = new can.Observe();
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
			view: '/static/process_interface/templates/process_detail.ejs',
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
		var $inputs = $pTable.find('button,input,textarea');
		var process = $pTable.data('process');
		var pId = process.attr('id');

		if ( pId ) {
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
				var sel = '[name="' + name + '"]';
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
				var sel = '[name="' + name + '"]';
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
				var sel = '[name="' + name + '"]';
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
				var sel = '[name="' + name + '"]';
				var ema = $pTable.find( sel ).closest('tr').data('emissionactivity');
				check_for_save.push( [ema, {value: emData[ name ]}] );
			}
		}

		for ( var i in check_for_save ) {
			var model = check_for_save[ i ][ 0 ];
			var data  = check_for_save[ i ][ 1 ];

			for ( var name in data ) {
				if ( ('' === data[ name ] && null === model[ name ])
					  || (data[ name ] == model[ name ] )
				) { // intentional double equals; compares "1" and 1 equal
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
			view: '/static/process_interface/templates/analysis_technology_detail.ejs',
		}
	},{
	init: function ( $el, options ) {  // AnalysisTechnologyDetail
		var view = options.view;
		if ( DEBUG )
			view += '?_=' + new Date().getTime();

		var t = options.technology;

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
		var is_list = this.options.technology.inputsplits;
		var os_list = this.options.technology.outputsplits;
		if ( is_list && is_list.length && is_list[0].isNew() )
			is_list[0].destroy();
		if ( os_list && os_list.length && os_list[0].isNew() )
			os_list[0].destroy();

		can.Control.prototype.destroy.call(this);
	},
	save: function ( $el ) {  // AnalysisTechnologyDetail
		var errors = {}
		  , $tForm  = null, tData  = null
		  , $isForm = null, isData = null
		  , $osForm = null, osData = null
		  , to_save = new Array();
		var $tTable = $el.closest('.technology');
		var $inputs = $tTable.find('button,input,textarea');
		var tech = $tTable.data('technology');
		var tId = tech.attr('id');

		if ( tId ) {
			$tForm  = $('#FormTechnology_' + tId);
			$isForm = $('#FormTechnologyInputSplits_' + tId);
			$osForm = $('#FormTechnologyOutputSplits_' + tId);
		} else {
			$tForm = $('#NewTechnologyForm');
		}

		$tTable.find('.error').empty(); // remove any previous error messages

		// 1. Collect the data
		if ( $tForm )
			tData = can.deparam( $tForm.serialize() );
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
				var sel = '[name="' + name + '"]';
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
				var sel = '[name="' + name + '"]';
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
	'[name="InputSplitRemove"] click': function ( $el, ev ) { // AnalysisTechnologyDetail
		$el.closest( 'tr' ).data('inputsplit').destroy();
	},
	'[name="OutputSplitRemove"] click': function ( $el, ev ) { // AnalysisTechnologyDetail
		$el.closest( 'tr' ).data('outputsplit').destroy();
	},
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
	$.cookie( COOKIE, JSON.stringify( $cookie ));

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
		var url = '/static/process_interface/js/QuickFunction.js';
		url += '?_=' + new Date().getTime();
		$.getScript( url )
		.fail( function ( ) {
			showStatus('Error reading quick function.  Typo?');
		});
	});
	$(document).bind('keyup', 'shift+space', function ( ) {
		$('#QuickFunction').trigger('click');
	});

	$('#ReloadLibs').click( function () { reloadLibs( false ); } );
	$(document).bind('keyup', 'ctrl+space', function () {
		reloadLibs();
	});
	$('#ShowHideAnalysis').click( function () {
		$('#analysis_detail').toggle( 'slide', {direction: 'up'} );
	});
	$('#ShowHideTechs').click( function () {
		$('#DBTechnologies').toggle( 'slide', {direction: 'down'} );
	});

	$(document).bind('keydown', 'shift', function ( e ) {
		hideStatus();
		showStatus('Showing remove buttons ...', 'info');
		setTimeout( function ( ) { $('.remove').removeClass('hidden'); }, 1 );
	});
	$(document).bind('keyup', 'shift', function ( e ) {
		hideStatus();
		showStatus('Hiding remove buttons ...', 'info');
		setTimeout( function ( ) { $('.remove').addClass('hidden'); }, 1 );
	});
}

$(document).ready( function () {
	BeginTemoaDBApp();
});

})();

console.log( 'TemoaLib loaded: ' + Date() );

