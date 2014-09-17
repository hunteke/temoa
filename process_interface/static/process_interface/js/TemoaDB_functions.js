;(function () {

"use strict";  // ECMA v5 pragma, similar to Perl's functionality.
  // FYI: http://ejohn.org/blog/ecmascript-5-strict-mode-json-and-more/

///////////////////////////////////////////////////////////////////////////////
//                       Miscellaneous helper functions                      //
///////////////////////////////////////////////////////////////////////////////


// Function borrowed from the Django Online documentation on CSRF:
// https://docs.djangoproject.com/en/dev/ref/contrib/csrf/
Temoa.fn.csrfSafeMethod = function ( method ) {
	// these HTTP methods do not require CSRF protection
	return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}


Temoa.fn.getCookie = function ( ) {
	var $obj = $.cookie( Temoa.C.COOKIE );
	if ( $obj ) {
		return JSON.parse( atob( $obj ));
	}

	$obj = new Object();
	$obj.username    = null;
	$obj.analysis_id = null;
	$obj.process_ids = null;

	return $obj;
}

Temoa.fn.setCookie = function ( obj ) {
	$.cookie( Temoa.C.COOKIE, btoa( JSON.stringify( obj )));
}


Temoa.fn.escapeHTML = function ( to_escape ) {
	var el = document.createElement('p');
	el.appendChild( document.createTextNode( to_escape ));
	return el.innerHTML;
}


Temoa.fn.replaceNamedArgs = function ( str, replacements ) {
	for ( var i in replacements ) {
		var arg = '{' + i + '}';
		if ( str.indexOf( arg ) > -1 ) {
			str = str.replace( new RegExp( arg, 'g' ), replacements[i] );
		}
	}
	return str;
}


Temoa.fn.disable = function ( list_of_inputs ) {
	for ( var i = 0; i < list_of_inputs.length; ++i ) {
		$(list_of_inputs[ i ]).attr('disabled', 'true');
	}
}


Temoa.fn.enable = function ( list_of_inputs ) {
	for ( var i = 0; i < list_of_inputs.length; ++i ) {
		$(list_of_inputs[ i ]).removeAttr('disabled');
	}
}


Temoa.fn.hideStatus = function( nxt_func ) {
	var $status = $('#status');
	$status.empty();
	$status.clearQueue().stop(true, true).fadeOut( 1 );
	$status.addClass( 'hidden' );
	if ( nxt_func ) { nxt_func(); }
}


Temoa.fn.showStatus = function ( msg, cssclass, safe_msg ) {
	var $st = $('<div>', {id: 'status'});
	if ( ! cssclass ) { cssclass = 'error' }

	if ( msg ) {
		msg = Temoa.fn.escapeHTML( msg );
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
	    $st.delay( 1000 ).fadeOut( 4000 ).queue( Temoa.fn.hideStatus );
	  },
	  'info' : function ( ) {
	    $st.clearQueue().stop(true, true).show().fadeIn( 1 ).delay( 1000 );
	    $st.fadeOut( 2000 ).queue( Temoa.fn.hideStatus );
	  }
	};
	actions[ cssclass ]();
	$('#status').replaceWith( $st );
}


Temoa.fn.clearAnalysisViews = function ( ) {
	$('#ProcessList .items').replaceWith(
		$('<div>', {class: 'items'}) );
	$('#ProcessDetails .items').replaceWith(
		$('<div>', {class: 'items'}) );
}


Temoa.fn.isInteger = function ( x ) {
	var _ceil = Math.ceil( Number(x) ), _floor = Math.floor( Number(x) );
	return (_ceil === _floor) && (_ceil === parseInt(x));
}


Temoa.fn.displayErrors = function ( $el, errors ) {
	// errors should be a dictionary-like object of arrays.
	if ( 'General Error' in errors ) {
		$el.find('.error').html( errors['General Error'] );
		delete errors['General Error'];
	}
	for ( var key in errors ) {
		var $err = $el.parent().find('.error');

		$el.focus(); // ideally only place at first input, but so what ...
		if ( ! $err.length ) {
			console.log( 'Warning: no errors displayed.  Element and Error ' +
			  'object: ', $el, errors );
		}
		for ( var i = 0; i < errors[key].length; ++i ) {
			$err.append( '<br />' + errors[key][i] );
		}
	}
}


Temoa.fn.save_to_server = function ( args ) {
	// Will save a list of [model, data] tuples to the server, weeding out
	// information that has not changed.  Thus, this sends only the minimal
	// amount of data.  For example, if a user changes just one field, it is
	// the only field sent.

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
			Temoa.fn.enable( $inputs );

			// "atomically" update model
			if ( model_copy.real_model.isNew() )
				model_copy.real_model.attr( new_data.attr() );
			else
				model_copy.real_model.attr( new_data );

			model_copy.real_model = null; // don't inadvertently remove real thing
			model_copy.attr({id: null}).destroy();

			Temoa.fn.showStatus('Saved!', 'info' );
		}, function ( jqXHR, text_status, description ) {
			Temoa.fn.enable( $inputs );
			model_copy.real_model = null; // don't inadvertently remove real thing
			model_copy.attr({id: null}).destroy();

			if ( jqXHR && jqXHR.responseJSON ) {
				Temoa.fn.displayErrors( $displayContainer, jqXHR.responseJSON );
			} else {
				console.log( 'Error received, but no JSON response: ', jqXHR );
				Temoa.fn.showStatus( 'Unknown error while saving data: ' + description );
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
			if ( ('' === data[ name ] && null == model[ name ])
				  || (data[ name ] == model[ name ] )
			) { // intentionally one triple equals; compares "1" and 1 equal
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
		Temoa.fn.showStatus( 'No changes; no need to talk to server.', 'info' );
		Temoa.fn.enable( args.inputs );
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


Temoa.fn.numericSort = function ( lhs, rhs ) { return lhs - rhs; }


Temoa.fn.processCookie = function ( ) {
	// These settings are set by the server.  Changing them -- maliciously or
	// otherwise -- will only affect the client experience.  From a security
	// perspective, they have no bearing on the choices the server makes.

	var $ss = $.cookie( 'ServerState' );
	if ( ! $ss ) { return; }

	var $ss = JSON.parse( atob( $.cookie( 'ServerState' )));

	var $cookie = Temoa.fn.getCookie();
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
	$.cookie( Temoa.C.COOKIE, btoa( JSON.stringify( $cookie )));

	// To "prove" the above point, remove the cookie sent by the server,
	// although one cookie ($cookie) is as good as another ($ss).
	$.removeCookie( 'ServerState', { 'path' : '/' } );
}

///////////////////////////////////////////////////////////////////////////////
//                               Event handlers                              //
///////////////////////////////////////////////////////////////////////////////

Temoa.eventHandler.update_timeslice = function ( mapping, oldKey ) {
	// Because the key is a timeslice name, and it is hardcoded by
	// the server, we need to update it if it changes.  Everything
	// would right itself if the user reloaded the page, but that
	// would get cumbersome.

	// Note that this operation requires it's own function so that
	// 'oldKey' is not bound via closure to an incorrect value.
	var timeslice = mapping.attr( oldKey ).attr('timeslice');
	timeslice.on('change',
		function ( ev, attr, how, newVal, oldVal ) {
		if ( 'set' !== how )
			return;

		var newName = timeslice.attr('name');
		var obj = mapping.attr( oldKey );
		mapping.attr( newName, obj );
		mapping.removeAttr( oldKey );
	});
}

///////////////////////////////////////////////////////////////////////////////
//                         Prototypes and Extensions                         //
///////////////////////////////////////////////////////////////////////////////

String.prototype.insert = function ( index, str ) {
	// Support negative indexing
	if ( index < 0 )
		index += this.length;
	return this.slice(0, index) + str + this.slice(index);
};

///////////////////////////////////////////////////////////////////////////////
//                            CAN helper functions                           //
///////////////////////////////////////////////////////////////////////////////

can.Model.prototype.clone = function ( ) {
	// Borrowed from: http://forum.javascriptmvc.com/topic/canjs-model-cloning
	var data = this.attr();
	delete data[ this.constructor.id ];
	return new this.constructor( data )
}

///////////////////////////////////////////////////////////////////////////////
//                                  Graphviz                                 //
///////////////////////////////////////////////////////////////////////////////

Temoa.fn.drawUnsolvedSystemDigraph = function ( ) {
	var processes = $('#ProcessList').data('processes');

	// Unfortunately, doing a straight jQuery tag creation ('$("<svg>")') doesn't
	// work currently as the <svg> tag is eventually created with
	// document.createElement, which defaults to the XHTML namespace rather than
	// the svg namespace.  This messes with the d3 rendering assumptions, so let
	// the browser figure out the correct semantics through it's normal parsing
	// routines by inserting the tag string instead.

	// Note also, that this implementation requires an <svg> element already
	// be in place.  A note for future test writers.  Ahem.
	$('#UnsolvedSystemMap').find('svg').first().replaceWith('<svg><g/></svg>');

	var energy_nodes = new Object(); // abusing for it's set-like attributes
	var tech_nodes = new Object();   // abusing for it's set-like attributes
	var unconnected_nodes = new Object();  // abusing for it's set-like attributes
	var inp_edges = new Object();    // abusing for it's set-like attributes
	var out_edges = new Object();    // abusing for it's set-like attributes
	for ( var i = 0; i < processes.length; ++i ) {
		var p = processes[ i ];
		var eff_list = p.efficiencies;
		var tech_name = p.technology.name;

		for ( var ei = 0; ei < eff_list.length; ++ei ) {
			var e = eff_list[ ei ];
			inp_edges[ e.inp + ' - ' + tech_name ] = 1;
			out_edges[ tech_name + ' - ' + e.out ] = 1;
			energy_nodes[ e.inp ] = 1;
			energy_nodes[ e.out ] = 1;
		}
		// utilize unconnected_nodes to make it obvious (through a CSS class) what
		// nodes have no efficiencies.
		if ( eff_list.length ) { tech_nodes[ tech_name ] = 1; }
		else                   { unconnected_nodes[ tech_name ] = 1; }
	}

	for ( var node in unconnected_nodes ) {
		if ( node in tech_nodes )
			delete unconnected_nodes[ node ];
	}

	if ( (0 === Object.keys( tech_nodes ).length) &&
	     (0 === Object.keys( energy_nodes ).length) &&
	     (0 === Object.keys( unconnected_nodes ).length) )
	{
		return;
	}

	var g = new dagreD3.Digraph();   // equivalent to 'digraph g {}'

	for ( var tech in tech_nodes ) { g.addNode( tech, {label: tech, 'class': 'node tech'} ); }
	for ( var form in energy_nodes ) { g.addNode( form, {label: form, 'class': 'node energy'} ); }
	for ( var node in unconnected_nodes ) { g.addNode( node, {label: node, 'class': 'node unconnected'} ); }
	for ( var i in inp_edges ) {
		var inp = i.split(' - ')[0], tech = i.split(' - ')[1];
		g.addEdge( null, inp, tech, {'class': 'edgePath input'} );
	}
	for ( var i in out_edges ) {
		var tech = i.split(' - ')[0], out = i.split(' - ')[1];
		g.addEdge( null, tech, out, {'class': 'edgePath output'} );
	}

	var layout = dagreD3.layout()
	  .nodeSep(20)
	  .rankDir("LR");
	var renderer = new dagreD3.Renderer();
	renderer.layout(layout).run(g, d3.select("#UnsolvedSystemMap svg g"));
}

})();
