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


Temoa.canControl.CommodityDetail = can.Control('CommodityDetail', {
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
	'{CommodityDemand} destroyed': function ( Model, ev, commodity ) {
		if ( this.commodity === commodity ) {
			var $div = this.element.find( '#CommodityForm_' + commodity.id );
			$div.remove();
		}
	},
	'{CommodityEmission} destroyed': function ( Model, ev, commodity ) {
		if ( this.commodity === commodity ) {
			var $div = this.element.find( '#CommodityForm_' + commodity.id );
			$div.remove();
		}
	},
	'{CommodityPhysical} destroyed': function ( Model, ev, commodity ) {
		if ( this.commodity === commodity ) {
			var $div = this.element.find( '#CommodityForm_' + commodity.id );
			$div.remove();
		}
	}
});

})();

console.log( 'TemoaDB CommodityDetail View loaded: ' + Date() );
