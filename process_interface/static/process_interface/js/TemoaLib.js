var COOKIE = 'TemoaDB_UISettings';

var logged_in = false;


function setCookie ( obj ) {
	$.cookie( COOKIE, JSON.stringify( obj ));
}

function getCookie ( ) {
	var $obj = $.cookie( COOKIE );
	if ( $obj ) {
		return JSON.parse( $obj );
	}

	$obj = jQuery( new Object() );
	$obj.selected_analysis  = null;
	$obj.selected_processes = null;
	$obj.selected_username  = null;

	return $obj;
}



// Function borrowed from the Django Online documentation on CSRF:
// https://docs.djangoproject.com/en/dev/ref/contrib/csrf/
function csrfSafeMethod ( method ) {
	// these HTTP methods do not require CSRF protection
	return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}


function escapeHTML ( to_escape ) {
	var el = document.createElement('p');
	el.appendChild( document.createTextNode( to_escape ));
	return el.innerHTML;
};


function hideStatus ( nxt_func ) {
	var $status = $('#status');
	$status.empty();
	$status.clearQueue().stop(true, true).fadeOut( 1 );
	$status.addClass( 'hidden' );
	if ( nxt_func ) { nxt_func(); }
}


function showStatus ( msg, cssclass ) {
	var $st = $('#status');
	if ( ! cssclass ) { cssclass = 'error' }

	msg = escapeHTML( msg );
	$st.addClass( cssclass );
	$st.removeClass( 'hidden' );
	$st.html( msg );
	var actions = {
	  'error': function ( ) {
	    $st.clearQueue().stop(true, true).show().fadeIn( 1 ).delay( 1000 );
	    // flash twice
	    $st.fadeOut().fadeIn().delay( 1000 ).fadeOut().fadeIn();
	    $st.delay( 1000 ).fadeOut( 4000 ).queue( hideStatus );
	  },
	  'info' : function ( ) {
	    $st.clearQueue().stop(true, true).show().fadeIn( 1 ).delay( 1000 );
	    $st.fadeOut( 2000 ).queue( hideStatus );
	  }
	};
	actions[ cssclass ]();
}


function addRow ( ) {
	var $button = $(this);

	var $tbody = $button.parents( 'tbody:first' );
	var $new_rows = $tbody.find( 'form.new' );
	if ( $new_rows.length > 0 ) {
		return;
	}

	var url = $button.data().url;
	var data = {}
	var $children = $tbody.children();
	if ( 1 === $children.length ) {
		// There is no header, so request one
		data['header'] = 'yes';
	}

	$.get( url, data )
	.done( function ( response_data, textStatus, jqXHR ) {
		var $newData = $( response_data );
		if ( 1 === $children.length ) {
			$tbody.append( $newData );
		} else {
			$( $tbody.children()[1]).after( $newData );
		}

		var $newForm = $newData.find('form');
		$newForm.submit( submitForm )
	});
}

function disable ( list_of_inputs ) {
	for ( var i = 0; i < list_of_inputs.length; ++i ) {
		$(list_of_inputs[ i ]).attr('disabled', 'true');
	}
}

function enable ( list_of_inputs ) {
	for ( var i = 0; i < list_of_inputs.length; ++i ) {
		$(list_of_inputs[ i ]).removeAttr('disabled');
	}
}

function submitForm ( ) {
	var $form = $(this);

	// First, serialize the data
	var to_submit = $form.serialize();

	// /then/ disable the form
	var inputs = $form.find('input');
	disable( inputs );
	var submit_url = $form.attr('action');

	$.post( submit_url, to_submit )
	.done( function ( response_data, textStatus, jqXHR ) {
		var $newData = $( response_data );
		var $newForm = $newData;

		if ( ! $newData.is( 'form' ) ) {
			$newForm = $newData.find( 'form' );
		}
		$form.replaceWith( $newForm );
		$newForm.submit( submitForm );
		$newForm.find('input[type="text"]:first').focus();
	})
	.fail( function ( jqXHR, textStatus, errorThrown ) {
		var server_msg = $( jqXHR ).attr( 'responseText' );
		$.get( '/session_messages/' )
		.done( function( response_data, textStatus, jqXHR ) {
			var $msgs = $( response_data );
			// Though response_data is an array, assume only one message
			var level = $msgs[0][0];
			var msg   = $msgs[0][1];

			showStatus( 'Unable to alter process.  Server said: ' + msg, level );
			enable( inputs );
		});
	});

	return false;  // don't submit through normal channels, please
}


function showProcessCharacteristics ( html_string ) {
	var $pcItems = $('#process_characteristics .items');
	$pcItems.empty();
	$pcItems.append( html_string );

	var $forms = $pcItems.find( 'form' );
	for ( var i = 0; i < $forms.length; ++i ) {
		var $form = $( $forms[ i ] );
		$form.submit( submitForm );
	}

	var $buttons = $pcItems.find( 'button.add' );
	for ( var i = 0; i < $buttons.length; ++i ) {
		var $button = $( $buttons[ i ] );
		$button.click( addRow );
	}

	$('#process_characteristics').removeClass('hidden');
}


function getProcessesInfo ( ) {
	// First, hide the process block to ensure that user is aware it's
	// changing
	$('#process_characteristics').addClass('hidden');
	$('#technology_characteristics').addClass('hidden');

	var process_ids = new Array();
	var $selected = $('#processes .items tbody tr.ui-selected');
	$.each( $selected, function ( index, row ) {
	  process_ids.push( $( row ).attr('data-processid') );
	});
	if ( process_ids.length > 0 ) {
		process_ids.sort( function(lhs, rhs) { return lhs - rhs; });
		ids = process_ids.join(',');
		var analysis_id = $('#filter_analyses_analysis').val();

		$.get( '/analysis/' + analysis_id + '/process_info/' + ids )
		.done( function ( response_data, textStatus, jqXHR ) {
			showProcessCharacteristics( response_data );
		});

		// With the request out, set the cookie in case the page is reloaded
		var $current = getCookie();
		$current.selected_processes = process_ids;
		setCookie( $current );

	}
}


function showProcesses ( data ) {
	var $tbody = $('<tbody/>');
	var noRow = 0;
	var css = ['even', 'odd'];
	for ( var i in data ) {
		id      = data[i][0];
		tech    = data[i][1];
		vintage = data[i][2];

		noRow += 1;
		$tr = $('<tr/>', { 'data-processid' : id, 'class' : css[noRow % 2] });
		$tr.append( $('<td/>').html( tech ) );
		$tr.append( $('<td/>').html( vintage ) );
		$tbody.append( $tr );
	}
	$('#processes .items tbody').replaceWith( $tbody );
	$('#processes .items tbody').selectable({ stop: getProcessesInfo });

	var $cookie = getCookie();
	if ( $cookie.selected_processes ) {
		for ( var i = 0; i < $cookie.selected_processes.length; ++i ) {
			id = $cookie.selected_processes[ i ];
			$('[data-processid="' + id + '"]').addClass( 'ui-selected' );
		}
		getProcessesInfo();
	}

	$('#processes').removeClass('hidden');
}


function selectAnalysis ( ) {
	var analysis_id = $('#filter_analyses_analysis').val();
	$.ajax({
	  url: '/analysis/' + analysis_id + '/process_list',
	  success: showProcesses
	});

	$.ajax({
	  url: '/analysis/' + analysis_id,
	  success: function ( analysis_metadata ) {
	    var $cookie = getCookie();
	    $cookie.selected_analysis = analysis_metadata;
	    setCookie( $cookie );
	  }
	});
}


function selectUser ( ) {
	// A selected user means we should update the list of analyses
	username = $('#filter_analyses_username').val();
	$.ajax({
	  url: '/user/' + username + '/analyses',
	  success: function ( data ) {
	    data = data[0];
	    var length = data.length;
	    var options = {};
	    for ( var i = 0; i < length; i += 2 ) {
	      key = data[ i ];
	      val = data[ i +1 ];
	      options[ key ] = val;
	    }
	    var $analyses = $('#filter_analyses_analysis');
	    $.each( options, function( val, text ) {
	      $analyses.append( $('<option/>').val( val ).html( text ));
	    });
	    $analyses.change( selectAnalysis );

	    if ( length > 0 ) {
	      selectAnalysis();
	    }
	  }
	});

	// With the request out, set the cookie in case the page is reloaded
	var $current = getCookie();
	$current.selected_username = username;
	setCookie( $current );
}


function updateUserList ( ) {
	$.get( '/user/list' )
	.done( function ( data ) {
		data = data[0];
		var length = data.length;
		var options = {};
		for ( var i = 0; i < length; i += 2 ) {
			key = data[ i ];
			val = data[ i +1 ];
			options[ key ] = val;
		}

		var $userlist = $('#filter_analyses_username');
		$.each( options, function( val, text ) {
			text = val + ' (' + text + ')';
			$userlist.append( $('<option/>').val( val ).html( text ));
		});

		$userlist.change( selectUser );

		var $cookie = getCookie();
		if ( $cookie.selected_username ) {
			$userlist.val( $cookie.selected_username );
			$userlist.change();
		}
	});
}


function BeginTemoaDBApp ( ) {
	// create clone after onChange registration of event
	var $body = $('body');
	if ( $body.data().username ) {
		logged_in = true;
	}

	// Begin: Code adapted from Django documentation on CSRF
	// var csrftoken = $body.data().csrftoken;
	// if ( typeof( csrftoken ) !== "undefined" ) {
	// 	$.ajaxSetup({
	// 	  crossDomain: false,  // There should be no need to talk elsewhere.
	// 	  beforeSend: function ( xhr, settings ) {
	// 	    if ( ! csrfSafeMethod( settings.type )) {
	// 	      xhr.setRequestHeader( 'X-CSRFToken', csrftoken );
	// 	    }
	// 	  }
	// 	});
	// } else {
	// 	var msg = 'There was an error with the a security token from the ';
	// 	msg += 'server.  Consequently, you will not be able to update any ';
	// 	msg += 'values, only browse the currently available data.  Please ';
	// 	msg += 'contact the Temoa Project (via a GitHub ticket, or the forums) ';
	// 	msg += 'if this is a problem for you.';
	// 	alert( msg );
	// }
	// End: borrowed code.

	// $body.keydown( hideAddShowRemove );
	// $body.keyup( function ( event ) { showAddHideRemove(); } );

	$('#ReloadLibs').click( function () { reloadLibs( false ); } );
	$(document).bind('keydown', 'ctrl+space', function () {
		reloadLibs( false );
	});
	//$(document).bind('keydown', 'shift',

	updateUserList();
}

console.clear();
console.log( 'TemoaLib loaded: ' + Date() );

