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


Temoa.canControl.AnalysisDetail = can.Control('AnalysisDetail', {
	defaults: {
			view: Temoa.C.ROOT_URL + '/client_template/analysis_info.ejs'
		}
	},{
	init: function ( $el, options ) {
		var view = options.view;
		if ( Temoa.C.DEBUG )
			view += '?_=' + new Date().getTime();

		var analysis = options.analysis;

		if ( ! analysis.commodity_emission )
			analysis.attr('commodity_emission',
			  new CommodityEmission.List() );
		if ( ! analysis.commodity_demand )
			analysis.attr('commodity_demand',
			  new CommodityDemand.List() );
		if ( ! analysis.commodity_physical )
			analysis.attr('commodity_physical',
			  new CommodityPhysical.List() );
		if ( ! analysis.segfracs )
			analysis.attr('segfracs', new SegFrac.List() );
		if ( ! analysis.future_periods )
			analysis.attr('future_periods', new can.List() );
		if ( ! analysis.all_vintages )
			analysis.attr('all_vintages', new can.List() );

		var view_opts = {
			username: Temoa.fn.getCookie().username || null,
			analysis: analysis,
		};

		$el.append( can.view( view, view_opts )).fadeIn();

		if ( analysis.isNew() )
			// a new analysis won't have anything attached to it ...
			return;

		Commodities.findAll( {aId: analysis.id},
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
				function update_periods ( ev, attr, how, newVal, oldVal ) {
					var new_vint_list = analysis.vintages.split(',');
					var fp_list = analysis.future_periods;
					var av_list = analysis.all_vintages;
					for ( var i = 0; i < new_vint_list.length; ++i )
						new_vint_list[ i ] = +new_vint_list[ i ];
					new_vint_list.sort( Temoa.fn.numericSort );

					fp_list.splice( 0 ); // remove all current elements
					av_list.splice( 0 ); // remove all current elements
					for ( var i = 0; i < new_vint_list.length -1; ++i ) {
						// -1 == last year, which is _not_ a period
						var year = +new_vint_list[ i ];
						av_list.push( year )
						if ( year < analysis.period_0 )
							continue;
						fp_list.push( year );
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
								fd = new Demand({
									aId:    analysis.id,
									cId:    dem.id,
									period: fp_list[ i ],
									commodity_name: dem.name
								});
							} else if ( ! fd.isNew ) {
								// CanJS doesn't convert non-List returned models, so we
								// need to explicitly make it a can.Model
								fd = new Demand( fd.attr() );
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
				var future_periods = analysis.future_periods || new can.List();
				var all_vintages   = analysis.all_vintages   || new can.List();
				var future_demands = analysis.future_demands || new can.Map();
				var segfracs = analysis.segfracs || new can.List();

				analysis.attr({
					commodity_emission: ce,
					commodity_demand:   cd,
					commodity_physical: cp,
					commodity_output:   c_output,  // to be union of cd & cp
					future_demands:     future_demands,
					all_vintages:       all_vintages,
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
				analysis.on('vintages', update_periods );
				analysis.on('vintages', update_future_demands );
				cd.on('change', update_future_demands );
				update_periods();
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
							dem = new Demand({
								aId: analysis.id,
								cId: dem_coms[ i ]['id'],
								period: future_periods[ i ],
								commodity_name: cname
							});
						} else if ( ! dem.isNew ) {
							// CanJS doesn't convert non-List returned models, so we
							// need to explicitly make it a can.Model
							dem = new Demand( dem.attr() );
						}
						dem_map.attr( dem_name, dem );
					}
				}

				for ( var sf_key in _segFracs ) {
					var ddd = ddd_map[ sf_key ];
					var sf = _segFracs[ sf_key ];
					if ( ! ddd ) {
						ddd = new DemandDefaultDistribution({
							aId: analysis.id,
							sfId: sf.attr('id')
						});
					} else if ( ! ddd.isNew ) {
						// Workaround a lacking feature in CanJS: there appears to
						// be no way to return a /dictionary/ of models via the
						// attributes plugin, only a can.List().  Unfortunately, we
						// only want random access for DDD.  So, we convert each
						// Map into a Model.
						ddd = new DemandDefaultDistribution( ddd.attr() );
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
							dist = new DemandSpecificDistribution({
								aId: analysis.id,
								dId: com['id'],
								sfId: sf['id'],
							});
						} else if ( ! dist.isNew ) {
							dist = new DemandSpecificDistribution(
							  dist.attr() );
						}
						dist.attr( 'timeslice', sf );
						dsd.attr( sf_key, dist );
						Temoa.eventHandler.update_timeslice( dsd, sf_key );
					}
				}

				new CommodityLists( '#Commodities', {
					analysis: analysis });

			}
		).fail( function ( error ) {
			console.log( error );
			Temoa.fn.showStatus( null, null, "Unknown error retrieving the Analysis' commodity list.  If you can recreate this error after <em>reloading</em> the page, please inform the Temoa Project developers.");
		});

		$el.find('#ShowHideCommodities').click( function ( ev ) {
			$('#Commodities').toggle( 'slide', { direction: 'left' });
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
		$el.find('#ShowHideUnsolvedSystemMap').click( function ( ev ) {
			var $div = $('#UnsolvedSystemMap');
			if ( $div.is(':hidden') ) {
				// currently closed, but user has requested it to be opened;
				// however, must draw, /after/ div is visible
				setTimeout( Temoa.fn.drawUnsolvedSystemDigraph, 1);
			}
			$div.toggle( 'slide', {direction: 'left'} );
		});
		setTimeout( function ( ) {
			// necessary to attach listener /after/ CanJS has finished, so
			// setTimeout to the rescue
			$('#UnsolvedSystemMapCloseButton').click( function ( ) {
				$('#ShowHideUnsolvedSystemMap').click();
			});
		}, 1 );
	},
	save: function ( $el ) {
		var errors = {};
		var $form = $el.closest('form');
		var inputs = $form.find(':input');
		var data = can.deparam( $form.serialize() );

		Temoa.fn.disable( inputs );
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
		if ( ! data.period_0 || ! Temoa.fn.isInteger( data.period_0 )) {
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
			Temoa.fn.enable( inputs );
			Temoa.fn.displayErrors( $form, errors );
			return;
		}

		var analysis = $el.closest('.analysis').data('analysis');
		var isNew = analysis.isNew();
		analysis.attr( data ).save( function ( model ) {
			Temoa.fn.enable( inputs );
			Temoa.fn.showStatus( 'Successfully saved.', 'info' );
		}, function ( xhr ) {
			Temoa.fn.enable( inputs );
			if ( xhr && xhr.responseJSON ) {
				Temoa.fn.displayErrors( $form, xhr.responseJSON );
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
		Temoa.fn.showStatus('Alteration cancelled', 'info');
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

})();

console.log( 'TemoaDB AnalysisDetail View loaded: ' + Date() );
