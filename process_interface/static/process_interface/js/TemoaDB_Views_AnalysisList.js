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


Temoa.canControl.Analyses = can.Control('Analyses', {
	defaults: {
			view: Temoa.C.ROOT_URL + '/client_template/analysis_list.ejs'
		}
	},{
	init: function ( $el, options ) {
		var view = options.view;
		if ( Temoa.C.DEBUG )
			view += '?_=' + new Date().getTime();

		var thisAnalyses = this;
		Temoa.fn.clearAnalysisViews()
		Analysis.findAll({}, function ( analyses ) {
			var username = Temoa.fn.getCookie().username || null;
			if ( username )
				analyses.unshift( new Analysis() );

			thisAnalyses.analyses = analyses
			var view_opts = {
				username: username,
				analyses: analyses
			}
			$el.html( can.view( view, view_opts ));
			$el.removeClass('hidden');

			var $cookie = Temoa.fn.getCookie();
			if ( $cookie.analysis_id ) {
				$('#analysis_selection').val( $cookie.analysis_id ).change();
			}

			Temoa.fn.showStatus('Analyses loaded.', 'info');
		}, function ( exception, data, status, xhr ) {
			if ( 'success' === status ) {
				console.log( exception );
				var msg = 'Potential programming error.  If you can recreate this ';
				msg += 'message after a page reload, please inform the ';
				msg += 'TemoaProject exactly how.  Library message: "';
				msg += exception.toString() + '"';
				Temoa.fn.showStatus( msg );
			} else {
				console.log( exception, data, status, xhr );
				Temoa.fn.showStatus( 'Unknown error retrieving analyses data.' );
			}
		});
	},
	'select change': function ( $el, event ) {
		Temoa.fn.clearAnalysisViews();
		var val = $el.val();
		var analysis;

		var $cookie = Temoa.fn.getCookie();
		$cookie.analysis_id = val;
		Temoa.fn.setCookie( $cookie );

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

})();

console.log( 'TemoaDB AnalysisList View loaded: ' + Date() );
