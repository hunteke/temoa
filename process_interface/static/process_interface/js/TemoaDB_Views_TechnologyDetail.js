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

function cellChangeWatcher ( canControl ) {
	// This wrapper function required so as to preserve the CanJS 'this'
	// variable in the save() function.  Otherwise, editableTableWidget
	// overrides 'this' to be the modified cell.
	return function ( evt, newValue ) {
		canControl.save( $(this), newValue );
	}
}

Temoa.canControl.TechnologyDetail = can.Control('TechnologyDetail', {
	defaults: {
			view_url: Temoa.C.ROOT_URL + '/client_template/TechnologyDetail.mustache',
		}
	},{
	init: function ( $el, options ) {  // TechnologyDetail
		var view_url = options.view_url;

		var analysis = options.analysis;
		var username = Temoa.fn.getCookie().username || null;

		if ( analysis.username !== username )
			// -9 == length of .mustache
			view_url = view_url.insert(-9, '_anonymous');

		if ( Temoa.C.DEBUG )
			view_url += '?_=' + new Date().getTime();

		var t = this.technology = options.technology;

		if ( ! t.capacityfactors )
			t.attr('capacityfactors', new TechnologyCapacityFactor.List());
		if ( ! t.inputsplits )
			t.attr('inputsplits', new TechnologyInputSplit.List());
		if ( ! t.outputsplits )
			t.attr('outputsplits', new TechnologyOutputSplit.List());

		var view_opts = { technology: t, analysis: analysis };
		$el.append( can.view( view_url, view_opts ));

		// With the view added to the dom, make values editable
		var table_types = ['GeneralAttributes', 'CapacityFactors', 'InputSplits',
		  'OutputSplits', 'MaxMinCapacities', 'ProcessAttributes'];
		for ( var i = 0; i < table_types.length; ++i ) {
			var sel = '#TechnologyDetail_' + table_types[ i ] + '_' + t.id;
			var $tab = $el.find( sel );

			// Make td elements editable (jquery-editable-table!)
			$tab.editableTableWidget();

			// 'this' refers to this can.Control instance
			$tab.find('td').on('change', cellChangeWatcher( this ) );
		}
	},
	destroy: function ( ) {  // TechnologyDetail
		var capfac_list = this.options.technology.capacityfactors;
		var is_list = this.options.technology.inputsplits;
		var os_list = this.options.technology.outputsplits;
		if ( capfac_list && capfac_list[0] && capfac_list[0].isNew() )
			capfac_list[0].destroy();
		if ( is_list && is_list.length && is_list[0].isNew() )
			is_list[0].destroy();
		if ( os_list && os_list.length && os_list[0].isNew() )
			os_list[0].destroy();

		can.Control.prototype.destroy.call(this);
	},
	save: function ( $el, newValue ) {
		// The save function is called by cellChangeWatcher (above)
		//  $el -> the jQuery-ized element; should be a <td>
		//  newValue is the new contents of the cell; a string

		// this function outsources a secondary function that knows
		// how to retrieve the information from each technology block; save_*
		var $tab = $el.closest('table');
		var param = $el.closest('tr').data('name');
		var func = $el.closest('table').attr('id');
		func = 'save_' + func.replace(/^\w+_([A-z]+)_\d+$/, '$1');

		$tab.find('.error').empty(); // remove any previous error messages

		this[func]( $el, newValue )
		.done( function ( newData, msg, jqXHR ) {
			Temoa.fn.showStatus('Successfully saved: ' + newData[ param ], 'info' );
		})
		.fail( function ( jqXHR, msg, reason ) {
			if ( jqXHR && jqXHR.responseJSON ) {
				Temoa.fn.displayErrors( $el, jqXHR.responseJSON );
			} else {
				console.log( 'Error received, but no JSON response: ', jqXHR );
				Temoa.fn.showStatus( 'Unknown error while saving data: ' + description );
			}
		});
	},
	save_ProcessAttributes: function ( $el, newValue ) {
		var $row = $el.closest('tr');
		var param = $row.data('name');  // e.g, 'costinvest' or 'loanlife'

		var id = $el.data('id');
		var data = {}
		data[param] = newValue;
		console.log( data );
		return this.technology.save_ProcessAttributes( id, data );
	},
	'[name="TechnologyCancel"] click': function ( $el, ev ) {  // TechnologyDetail
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
	'[name="TechnologyUpdate"] click': function ( $el, ev ) {  // TechnologyDetail
		this.save( $el );
	},
	'[name="TechnologyCreate"] click': function ( $el, ev ) {  // TechnologyDetail
		this.save( $el );
	},
	'input keyup': function ( $el, ev ) {  // TechnologyDetail
		if ( 13 === ev.keyCode ) { // 13 == enter
			this.save( $(ev.target) );
		}
	},
	'[name="AddCapacityFactorTech"] click': function ( $el, ev ) {  // TechnologyDetail
		var capfac_list = this.options.technology.capacityfactors;
		if ( capfac_list && capfac_list.length && capfac_list[0].isNew() ) {
			// only one new CF at a time.
			return;
		}

		var tOpts = this.options;
		var opts = { aId: tOpts.analysis.id, tId: tOpts.technology.id };

		// Create the client-side version, then display it.
		var newCF = new TechnologyCapacityFactor( opts );
		capfac_list.unshift( newCF );
	},
	'[name="AddInputSplit"] click': function ( $el, ev ) {  // TechnologyDetail
		var is_list = this.options.technology.inputsplits;
		if ( is_list && is_list.length && is_list[0].isNew() ) {
			// only one new split at a time.
			return;
		}

		var tOpts = this.options;
		var opts = { aId: tOpts.analysis.id, tId: tOpts.technology.id };
		var newIS = new TechnologyInputSplit( opts );
		is_list.unshift( newIS );
	},
	'[name="AddOutputSplit"] click': function ( $el, ev ) { // TechnologyDetail
		var os_list = this.options.technology.outputsplits;
		if ( os_list && os_list.length && os_list[0].isNew() ) {
			// only one new split at a time.
			return;
		}

		var tOpts = this.options;
		var opts = { aId: tOpts.analysis.id, tId: tOpts.technology.id };
		var newOS = new TechnologyOutputSplit( opts );
		os_list.unshift( newOS );
	},
	'[name="CapacityFactorTechRemove"] click': function ( $el, ev ) { // TechnologyDetail
		$el.closest( 'tr' ).data('capacityfactor').destroy();
	},
	'[name="InputSplitRemove"] click': function ( $el, ev ) { // TechnologyDetail
		$el.closest( 'tr' ).data('inputsplit').destroy();
	},
	'[name="OutputSplitRemove"] click': function ( $el, ev ) { // TechnologyDetail
		$el.closest( 'tr' ).data('outputsplit').destroy();
	},
	'{TechnologyCapacityFactor} created' : function ( list, ev, obj ) {
		var segfracs = this.options.analysis.segfracs;
		for ( var i = 0; i < segfracs.length; ++i ) {
			if ( segfracs[ i ].id === obj.sfId )
				obj.attr('segfrac', segfracs[ i ] );
		}
	},
});

})();

console.log( 'TemoaDB TechnologyDetail View loaded: ' + Date() );
