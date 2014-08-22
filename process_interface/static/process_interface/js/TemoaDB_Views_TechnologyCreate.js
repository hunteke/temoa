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


Temoa.canControl.TechnologyCreate = can.Control('TechnologyCreate', {
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

})();

console.log( 'TemoaDB TechnologyCreate View loaded: ' + Date() );
