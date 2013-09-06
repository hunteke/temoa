var COOKIE = 'TemoaDB_UISettings';

function getCookie ( ) {
	var $obj = $.cookie( COOKIE );
	if ( $obj ) {
		return JSON.parse( $obj );
	}

	$obj = jQuery( new Object() );
	$obj.username    = null;
	$obj.analysis_id = null;
	$obj.process_ids = null;

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
	var inputs = $form.find('input,textarea');
	disable( inputs );
	var submit_url = $form.attr('action');

	$.post( submit_url, to_submit )
	.done( function ( response_data, textStatus, jqXHR ) {
		var $newData = $( response_data );
		var $newForm = $newData;

		if ( ! $newForm.is( 'form' ) ) {
			$newForm = $newData.find( 'form' );
		}
		$form.replaceWith( $newForm );
		$newForm.submit( submitForm );
		$newForm.find('input[type="text"]:first').focus();
	})
	.fail( function ( jqXHR, textStatus, errorThrown ) {
		var $html = $( $( jqXHR ).attr('responseText') );
		if ( $html.is( 'form' ) ) {
			$form.replaceWith( $html );
			$html.submit( submitForm );
			$html.find('tr[class="error"] input[type="text"]:first ').focus();
		}
		$.get( '/session_messages/' )
		.done( function( response_data, textStatus, jqXHR ) {
			var $msgs = $( response_data );
			// Though response_data is an array, assume only one message
			var level = $msgs[0][0];
			var msg   = $msgs[0][1];

			showStatus( 'Unable to make change.  Server said: ' + msg, level );
			enable( inputs );
		});
	})
	.always( function ( ) {
		// reattach any change listeners
		attachGlobalEventListeners()
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
		var analysis_id = getCookie().analysis_id;

		$.get( '/analysis/' + analysis_id + '/process_info/' + ids )
		.done( function ( response_data, textStatus, jqXHR ) {
			showProcessCharacteristics( response_data );
		});
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
	if ( $cookie.process_ids ) {
		for ( var i = 0; i < $cookie.process_ids.length; ++i ) {
			var id = $cookie.process_ids[ i ];
			$('[data-processid="' + id + '"]').addClass( 'ui-selected' );
		}
		getProcessesInfo();
	}

	$('#processes').removeClass('hidden');
}


function attachGlobalEventListeners ( ) {
	$('#analysis_selection').change( selectAnalysis );
}

function showAnalysis ( html_string ) {
	var $html = $( html_string );
	if ( $html.is( 'form' ) ) {
		$html.submit( submitForm );
	}

	var $aInfo = $('#analysis_info');
	$aInfo.empty().append( $html );

	attachGlobalEventListeners();
	$aInfo.removeClass('hidden');
}


function selectAnalysis ( ) {
	var analysis_id = $('#analysis_selection').val();
	if ( ! analysis_id ) { return; }

	$('#processes').addClass('hidden');
	$('#analysis_info').addClass('hidden');

	var url = '/analysis/' + analysis_id;

	var $cookie = getCookie();

	$.get( url )
	.done( function ( response_data, textStatus, jqXHR ) {
		showAnalysis( response_data );
	});

	if ( "New" === analysis_id ) { return; }

	$.get( url + '/process_list' )
	.done( function ( response_data, textStatus, jqXHR ) {
		showProcesses( response_data );
	});

}


function updateAnalysisList ( ) {
	var url = '/analysis/list';
	$.get( url )
	.done( function ( response_data, textStatus, jqXHR ) {
		var $cookie = getCookie();
		var aId = null;
		if ( $cookie.analysis_id ) {
			aId = $cookie.analysis_id;
		}
		console.log( "aId: " + aId );

		var $as = $('#analysis_selection');
		$as.empty().append( response_data ).change( selectAnalysis );

		console.log( 'HERE' );
		if ( aId ) {
			console.log( 'THERE' );
			$as.val( aId );
			$as.change();
		}
		$('#analysis_info').removeClass('hidden');
	});
}

function processCookie ( ) {
	// These settings are set by the server.  Changing them -- maliciously or
	// otherwise -- will only affect the client experience.  From a security
	// perspective, they have no bearing on the choices the server makes.

	var $ss = JSON.parse( atob( $.cookie( 'ServerState' )));
	var $cookie = getCookie();
	if ( 'analysis_id'   in $ss ) { $cookie.analysis_id   = $ss.analysis_id; }
	if ( 'process_ids'   in $ss ) { $cookie.process_ids   = $ss.process_ids; }

	if ( 'username'      in $ss ) {
		$cookie.username      = $ss.username;
		if ( $cookie.username ) { $('#unauthorized').addClass('hidden'); }
		else                    { $('#unauthorized').removeClass('hidden'); }
	}
	$.cookie( COOKIE, JSON.stringify( $cookie ));

	// To prove the above point, remove the cookie sent by the server
	$.removeCookie( 'ServerState', { 'path' : '/' } );
}

function BeginTemoaDBApp ( ) {
	// create clone after onChange registration of event
	var $body = $('body');

	$.ajaxSetup({
		crossDomain: false, //there should be no need to talk elsewhere
		complete: function( jqXHR, textStatus ) {
			processCookie( jqXHR );
		}
	});

	$('#ReloadLibs').click( function () { reloadLibs( false ); } );
	$(document).bind('keydown', 'ctrl+space', function () {
		reloadLibs( false );
	});
	//$(document).bind('keydown', 'shift',

	updateAnalysisList();
}

console.clear();
console.log( 'TemoaLib loaded: ' + Date() );

