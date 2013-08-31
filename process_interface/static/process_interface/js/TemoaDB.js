function reloadLibs ( is_initial_load ) {
	// By wrapping the loading of the helper files inside this function, we can
	// dynamically reload the library during development, rather than having to
	// reload the whole page.  Much quicker

	// First, the CSS
	var queryString = '?_=' + new Date().getTime();
	$('link[rel="stylesheet"]').each( function ( ) {
		this.href = this.href.replace(/\?.*|$/, queryString);
	});

	// Then the JS.
	$.getScript('/static/process_interface/js/TemoaLib.js')
	.done( function ( script, textStatus ) {
		if ( is_initial_load ) {
			BeginTemoaDBApp();
			console.log( 'Begin TemoaDB' );
		}
	});
}

$( document ).ready( function () {
	reloadLibs( true );
});
