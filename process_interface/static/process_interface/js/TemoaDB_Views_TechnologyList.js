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


Temoa.canControl.TechnologyList = can.Control('TechnologyList', {
	defaults: {
			view_url: Temoa.C.ROOT_URL + '/client_template/TechnologyList.mustache',
		}
	},{
	init: function ( $el, options ) {
		// $el -> the element to which this view is attached.  Removing this
		//        element will tell CanJS to cleanup all associated references.
		var view_url = options.view_url;

		var analysis = options.analysis;
		var username = Temoa.fn.getCookie().username || null;

		if ( analysis.username !== username )
			// -9 == length of .mustache
			view_url = view_url.insert(-9, '_anonymous');

		if ( Temoa.C.DEBUG )
			view_url += '?_=' + new Date().getTime();

		Technology.findAll( {aId: analysis.id}, function ( technologies ) {
			options['technologies'] = technologies;

			var view_opts = { technologies: technologies };
			$el.empty().append( can.view( view_url, view_opts ));

			var $tbody = $el.find('.items:first tbody');

			$tbody.selectable( {} );
			$tbody.on( 'selectablestart', function () {
				$('#TechnologyDetails .items').fadeOut();
			});
			$tbody.on( 'selectablestop', function () {
				function createTechnologyDetailBlocks ( toCreate ) {
					// Wrap the actual creation of each technology block within a
					// setTimeout list traversal so that each technology detail
					// block can display when it's ready.  This way, the user will
					// immediately see results, even for large selections.  This
					// also presents a graduated fade-in effect that some may find
					// pleasing.
					var $div = $('<div>', {id: 'TechnologyDetail_' + t.id});
					var control_opts = {
					  technology: toCreate.shift(),
					  analysis: analysis
					}

					new TechnologyDetail( $div, control_opts );
					$tdItems.append( $div );  // add to DOM /after/ creation

					if ( toCreate.length > 0 ) {
						setTimeout( function () {
							createTechnologyDetailBlocks( toCreate );
						}, 50 );  // 50 = something tiny; i.e., "reluinquish thread"
					}
				}

				var $info = $('#TechnologyDetails .items');

				var $sel = $( this ).find( 'tr.ui-selected' );
				var to_display = new Array();
				var ids        = new Array();
				for ( var i = 0; i < $sel.length; ++i ) {
					// must override class for each cell or the nth-child CSS for
					// the row will win.
					$($sel[i]).find('td').addClass('ui-selected');
					var t = $($sel[i]).data().technology
					to_display.push( t );
					ids.push( t.id );
				}

				// Set the ids in the cookie so that if a page reload occurs,
				// TemoaDB can automatically reselect these technologies.
				ids.sort( Temoa.fn.numericSort );
				var $cookie = Temoa.fn.getCookie();
				$cookie.technology_ids = ids
				Temoa.fn.setCookie( $cookie );

				var username = $cookie.username || null;

				var $tdItems = $('#TechnologyDetails .items');

				if ( ! to_display.length ) {
					// Nothing to display.  If the first child is a new technology,
					// then remove all others, but leave it.
					var children = $tdItems.children();
					if ( children.length ) {
						var first_child = $(children[0]).find('.technology');
						if ( first_child.data('technology').isNew() ) {
							$tdItems.children().not( children[0] ).remove();
							$tdItems.fadeIn();
						} else {
							$tdItems.empty();
						}
					}
				} else { // something to display
					var view_opts = {
						analysis: analysis,
						username: username,
					}

					$el.removeClass('hidden').fadeIn();
					// remove any child divs so browser can GC.
					$tdItems.empty();


					createTechnologyDetailBlocks( to_display );
				}
			});

			new TechnologyCreate('#technology_create', {
				technologies: technologies
			});
			// Pre-select what was selected in this session.
			// (Handy if the page needs to reload.)
			var $cookie = Temoa.fn.getCookie();
			if ( $cookie.technology_ids ) {
				var ids = $cookie.technology_ids;

				var sel = '[data-id="' + ids.join('"],[data-id="') + '"]';
				$tbody.find( sel ).addClass('ui-selected');
				$tbody.find( sel ).find('td').addClass('ui-selected');
				$tbody.trigger('selectablestop')
			}
		});
	},
	'{Technology} created': function ( list, ev, technology ) {
		this.options.technologies.unshift( technology );
	},
	'[name="RemoveTechnology"] click': function ( $el, ev ) {
		$el.closest( 'tr' ).data('technology').destroy();
	}
});

})();

console.log( 'TemoaDB TechnologyList View loaded: ' + Date() );
