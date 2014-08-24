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


Temoa.canControl.AnalysisParameters = can.Control('AnalysisParameters', {
	defaults: {
			view: Temoa.C.ROOT_URL + '/client_template/analysis_parameters.ejs'
		}
	},{
	init: function ( $el, options ) {
		var view = options.view;
		if ( Temoa.C.DEBUG )
			view += '?_=' + new Date().getTime();

		this.analysis = this.options.analysis
		$el.html( can.view( view, {
			analysis: this.analysis,
			username: Temoa.fn.getCookie().username || null,
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

		segfracs.unshift( new SegFrac({ aId: this.analysis.id }));
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
				Temoa.fn.showStatus( msg, 'info' );

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

		var $sfForm = $( 'form#SegFracs_' + aId );
		var $ddForm = $( 'form#DemandDefaultDistribution_' + aId );
		var $sfTable = $el.closest('.segfracs');
		var $inputs = $sfTable.find(':input').not("[disabled='disabled']");
		var sfData  = can.deparam( $sfForm.serialize() );
		var ddData  = can.deparam( $ddForm.serialize() );

		$sfTable.find('.error').empty(); // remove any previous attempt's errors
		Temoa.fn.disable( $inputs );

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
			Temoa.fn.enable( $inputs );
			Temoa.fn.displayErrors( $sfTable, errors );
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

		Temoa.fn.save_to_server({ to_save: to_save, inputs: $inputs, display: $sfTable });
	},
	saveDemands: function ( $el ) {  // AnalysisParameters
		var aId = this.analysis.id;
		var errors  = {};
		var to_save = new Array();
		var to_remove = new Array();
		var demand_name_re = /^([A-z_]\w*), (\d+)$/;  // not flexible on space.

		var $form = $( 'form#Demands_' + aId );
		var $demTable = $el.closest('.demands');
		var $inputs = $demTable.find(':input').not("[disabled='disabled']");
		var data = can.deparam( $form.serialize() );

		$demTable.find('.error').empty(); // remove any previous attempt's errors
		Temoa.fn.disable( $inputs );

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
			Temoa.fn.enable( $inputs );
			Temoa.fn.displayErrors( $demTable, errors );
			return;
		}

		for ( var name in data ) {
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

			dem.destroy( function ( destroyed_model ) {
				// Succeeded.  Now kill id and value locally.  Accordingly, there
				// is no need to create a new dem object.
				this.attr({id: null, value: null});

				var $el = $('.demands ' + this.sel);
				delete this.sel;
			}, function ( jqXHR, text_status, description ) {
				this._el.animate({backgroundColor: '#f00'
				      }).animate({backgroundColor: 'transparent'});
				this._el = null;
				delete this._el;

				if ( jqXHR && jqXHR.responseJSON ) {
					Temoa.fn.displayErrors( $dsdTable, jqXHR.responseJSON );
				} else {
					console.log( 'Error received, but no JSON response: ', jqXHR );
					Temoa.fn.showStatus( 'Unknown error while removing demand: '
					  + description );
				}
			});
		}

		Temoa.fn.save_to_server({ to_save: to_save, inputs: $inputs, display: $demTable });
	},
	saveDemandSpecificDistributions: function ( $el ) {  // AnalysisParameters
		var aId = this.analysis.id;
		var errors  = {};
		var to_save = new Array();
		var to_remove = new Array();
		var dsd_name_re = /^DSD_value_(\d+),(\d+)$/;

		var $form = $( 'form#DemandSpecificDistribution_' + aId );
		var $dsdTable = $el.closest('.demandspecificdistributions');
		var $inputs = $dsdTable.find(':input').not("[disabled='disabled']");
		var data = can.deparam( $form.serialize() );

		$dsdTable.find('.error').empty(); // remove any previous attempt's errors
		Temoa.fn.disable( $inputs );

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
			Temoa.fn.enable( $inputs );
			Temoa.fn.displayErrors( $dsdTable, errors );
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
				var new_d = new DemandSpecificDistribution({
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
					Temoa.fn.displayErrors( $dsdTable, jqXHR.responseJSON );
				} else {
					console.log( 'Error received, but no JSON response: ', jqXHR );
					Temoa.fn.showStatus( 'Unknown error while removing distribution: '
					  + description );
				}
			});
		}

		Temoa.fn.save_to_server({ to_save: to_save, inputs: $inputs, display: $dsdTable });
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

		ddd = new DemandDefaultDistribution({
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
		Temoa.fn.showStatus('Alteration cancelled', 'info');
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
		Temoa.fn.showStatus('Alteration cancelled', 'info');
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
		Temoa.fn.showStatus('Alteration cancelled', 'info');
	},
	'input keyup': function ( $el, ev ) {
		if ( ! $el.attr('form') )
			return;

		if ( 13 === ev.keyCode ) { // enter
			var formAttr = $el.attr('form');
			if ( 0 === formAttr.indexOf( 'SegFracs_' )
			  || 0 === formAttr.indexOf( 'DemandDefaultDistribution_' ))
			{
				this.saveSegFracs( $el );
			} else if ( 0 === formAttr.indexOf( 'Demands_' )) {
				$('[name="DemandsUpdate"]').click();
			} else if ( 0 === formAttr.indexOf( 'DemandSpecificDistribution_' )) {
				this.saveDemandSpecificDistributions( $el );
			}
		} else if ( 27 === ev.keyCode ) {  // escape
			var formAttr = $el.attr('form');

			if ( 0 === formAttr.indexOf( 'SegFracs_' )
			  || 0 === formAttr.indexOf( 'DemandDefaultDistribution_' ))
			{
				$el.closest('.segfracs').find('[name="SegFracCancel"]').click();
			}
			if ( 0 === formAttr.indexOf( 'Demands_' )) {
				$el.closest('.demands').find('[name="DemandsCancel"]').click();
			}
			if ( 0 === formAttr.indexOf( 'DemandSpecificDistribution_' )) {
				$el.closest('.demandspecificdistributions').find('[name="DemandSpecificDistributionCancel"]').click();
			}
		}
	},
	'{SegFrac} created': function ( list, ev, segfrac ) {
		var slice_name = segfrac.name();
		var ddd = new DemandDefaultDistribution({
			aId: this.analysis.id,
			sfId: segfrac.id,
		});
		this.analysis.demanddefaultdistribution.attr( slice_name, ddd );
	},
});

})();

console.log( 'TemoaDB AnalysisParameters View loaded: ' + Date() );
