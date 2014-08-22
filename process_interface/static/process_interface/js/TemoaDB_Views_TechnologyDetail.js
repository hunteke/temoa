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


Temoa.canControl.TechnologyDetail = can.Control('AnalysisTechnologyDetail', {
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

})();

console.log( 'TemoaDB TechnologyDetail View loaded: ' + Date() );
