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
			console.log( 'WEEEE' );
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
		var analysis_id = getCookie().selected_analysis.id;

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


function showAnalysis ( html_string ) {
	var $html = $( html_string );
	if ( $html.is( 'form' ) ) {
		$html.submit( submitForm );
	}

	var $aInfo = $('#analysis_info');
	$aInfo.empty().append( $html );

	$aInfo.removeClass('hidden');
}


function selectAnalysis ( ) {
	var analysis_id = $('#analysis_selection').val();
	$('#processes').addClass('hidden');
	$('#analysis_info').addClass('hidden');

	if ( ! analysis_id ) { return; }

	var url = '/analysis/' + analysis_id;

	var $cookie = getCookie();
	$cookie.selected_analysis = null
	setCookie( $cookie );

	$.get( url )
	.done( function ( response_data, textStatus, jqXHR ) {
		// $cookie.selected_analysis = response_data;
		// setCookie( $cookie );
		var $cookie = getCookie();
		$cookie.selected_analysis = {'id': 1};
		setCookie( $cookie );

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
		if ( $cookie.selected_analysis ) {
			aId = $cookie.selected_analysis.id;
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
	})

}


function BeginTemoaDBApp ( ) {
	// create clone after onChange registration of event
	var $body = $('body');
	if ( $body.data().username ) {
		logged_in = true;
	}

	$('#ReloadLibs').click( function () { reloadLibs( false ); } );
	$(document).bind('keydown', 'ctrl+space', function () {
		reloadLibs( false );
	});
	//$(document).bind('keydown', 'shift',

	updateAnalysisList();
}

console.clear();
console.log( 'TemoaLib loaded: ' + Date() );

