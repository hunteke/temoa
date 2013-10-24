"use strict";  // ECMA v5 pragma, similar to Perl's functionality.
  // FYI: http://ejohn.org/blog/ecmascript-5-strict-mode-json-and-more/

(function () {
var COOKIE = 'TemoaDB_UISettings';

var hoverEl = null;

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


function showStatus ( msg, cssclass, safe_msg ) {
	var $st = $('<div>', {id: 'status'});
	if ( ! cssclass ) { cssclass = 'error' }

	if ( msg ) {
		msg = escapeHTML( msg );
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
	    $st.delay( 1000 ).fadeOut( 4000 ).queue( hideStatus );
	  },
	  'info' : function ( ) {
	    $st.clearQueue().stop(true, true).show().fadeIn( 1 ).delay( 1000 );
	    $st.fadeOut( 2000 ).queue( hideStatus );
	  }
	};
	actions[ cssclass ]();
	$('#status').replaceWith( $st );
}


function showRemoveButtons ( show_remove_buttons, el ) {
	var $target = null
	if ( el ) {
		$target = $(el);
	} else if ( hoverEl ) {
		$target = $(hoverEl);
	} else {
		return;  // nothing to do!
	}

	var $to_hide, $to_show;
	if ( show_remove_buttons ) {
		$to_hide = $target.find('button.add');
		$to_show = $target.find('button.remove.hidden');
	} else {
		$to_hide = $target.find('button.remove');
		$to_show = $target.find('button.add.hidden');
	}

	for ( var i = 0; i < $to_hide.length; ++i ) {
		$($to_hide[i]).addClass( 'hidden' );
	}
	for ( var i = 0; i < $to_show.length; ++i ) {
		$($to_show[i]).removeClass( 'hidden' );
	}
};


function addProcessDataRow ( ) {
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
		$newForm.submit( submitForm );
	});
}

function addNewProcessRow ( ) {
	var $button = $(this);

	var $tbody = $button.parents('table:first').children( 'tbody' );
	var $new_rows = $tbody.find( 'tr.new' );
	if ( $new_rows.length > 0 ) { return; }

	var url = $button.data().url;
	$.get( url )
	.done( function ( response_data, textStatus, jqXHR ) {
		// refind: it may have changed since we loaded the button, or
		// concurrent to performing this operation.
		var $row = $( response_data );
		var $tbody = $button.parents('table:first').children( 'tbody' );

		$row.find('button').click( function() {
			$row.remove()
		});

		$tbody.prepend( $row );
	});
}


function removeProcessRow ( ) {
	var $button = $(this);

	var url = $button.data().url;
	var csrf = $button.parents('form').find('[name="csrfmiddlewaretoken"]');
	csrftoken = csrf.val();

	var req = $.ajax({
		url: url,
		type: 'DELETE',
		dataType: 'html',
		beforeSend: function ( xhr, settings ) {
			if ( ! csrfSafeMethod( settings.type )) {
				// if-block not specifically necessary, but following pattern
				xhr.setRequestHeader( 'X-CSRFToken', csrftoken );
			}
		}
	});

	req.done( function ( data, textStatus, jqXHR ) {
		showProcessList( data );
		showStatus( 'Process successfully removed.', 'info' );
	});
	req.fail( function ( jqXHR, textStatus ) {
		var msg = 'Unable to remove process from database.  Server said: ';
		showStatus( msg + textStatus );
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
		enable( inputs ); // Let user fix error if server not replacing form.
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
		attachGlobalEventListeners();
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
		$button.click( addProcessDataRow );
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
		var ids = process_ids.join(',');
		var analysis_id = getCookie().analysis_id;

		$.get( '/analysis/' + analysis_id + '/process_info/' + ids )
		.done( function ( response_data, textStatus, jqXHR ) {
			showProcessCharacteristics( response_data );
		});
	}
}


function attachProcessListEvents ( ) {
	var $items = $('#processes .items');
	var $thead = $items.children('thead');
	var $tbody = $items.children('tbody');

	$tbody.selectable({ 'stop': getProcessesInfo });

	var $cookie = getCookie();
	if ( $cookie.process_ids ) {
		var ids = $cookie.process_ids;
		var do_load = false;
		var sel = '[data-processid="' + ids.join('"],[data-processid="') + '"]';
		var $selected = $tbody.find( sel );

		for ( var i = 0; i < $selected.length; ++i ) {
			var $el = $($selected[ i ] );
			if ( ! $el.hasClass( 'ui-selected' ) ) {
				do_load = true;
				$el.addClass('ui-selected');
			}
		}
		if ( do_load ) {
			getProcessesInfo();
		}
	}

	var $buttons = $thead.find( 'button.add' );
	$buttons.off();
	for ( var i = 0; i < $buttons.length; ++i ) {
		var $button = $( $buttons[ i ] );
		$button.click( addNewProcessRow );
	}

	$buttons = $tbody.find( 'button.remove' );
	$buttons.off()
	for ( var i = 0; i < $buttons.length; ++i ) {
		var $button = $( $buttons[ i ] );
		$button.click( removeProcessRow );
	}

	$buttons = $tbody.find( 'button.cancel' );
	$buttons.off()
	for ( var i = 0; i < $buttons.length; ++i ) {
		var $button = $( $buttons[ i ] );
		$button.click( function() { $(this).parents('tr:first').remove(); });
	}

	var $form = $thead.parents('form');
	if ( $form ) {
		$form.off()
		$form.submit( submitForm );
	}

	var $tr = $items.find('tr');
	$tr.off();
	$tr.mouseenter( function() { hoverEl = this; });
	$tr.mouseleave( function() {
		if ( hoverEl === this ) {
			hoverEl = null;
		}
		showRemoveButtons( false, this );
	});
}


function showProcessList ( html_string ) {
	var $items = $('#processes .items');
	$items.replaceWith( html_string );

	attachProcessListEvents();

	$('#processes').removeClass('hidden');
}


function attachGlobalEventListeners ( ) {
	$('#analysis_selection').off().change( selectAnalysis );
	attachProcessListEvents();
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
		showProcessList( response_data );
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

		var $as = $('#analysis_selection');
		$as.empty().append( response_data ).change( selectAnalysis );

		if ( aId ) {
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

	var $ss = $.cookie( 'ServerState' );
	if ( ! $ss ) { return; }

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
			var status = jqXHR.status;
		},
		beforeSend: function ( xhr, settings ) {
			if ( ! csrfSafeMethod( settings.type )) {
				xhr.setRequestHeader( 'X-CSRFToken', $.cookie('csrftoken') );
			}
		},
		error: function ( jqXHR, textStatus, errorThrown ) {
			var status = jqXHR.status
			  , msg = null;
			if ( status >= 500 ) {
				if ( 501 === status ) {
					msg = "<p>501 (not implemented) - This message implies that you are testing new TemoaDB functionality, and that we have not implemented it yet.  If this is functionality you believe would be extremely helpful to your workflow, please let us know on the <a href='https://groups.google.com/forum/#!forum/temoa-project' title='GoogleGroups forum'>Temoa Project forum</a>.</p>";
				} else if ( 502 === status ) {
					msg = "<p>502 (bad gateway) - Some computer on the network that is between TemoaDB and your browser is having trouble communicating with us.  Hopefully this is a transient error, but if not, you may try connecting to TemoaDB from a different place.  Try contacting your local IT support for help, or accessing TemoaDB from a (different) coffee shop.</p>";
				} else if ( 503 === status ) {
					msg = "<p>503 (service unavailable) - The TemoaDB server is either offline for maintenance, or is overwhelmed by users.  Given the number of folks who know about TemoaDB, the former is most likely the issue.  If TemoaDB does not come back after a business day, consider inquiring on the <a href='https://groups.google.com/forum/#!forum/temoa-project' title='GoogleGroups forum'>Temoa Project forum</a>.</p>";
				} else if ( 504 === status ) {
					msg = "<p>504 (gateway timeout) - Some computer between TemoaDB and your browser did not receive a response from TemoaDB in a timely fashion.  This most likely means a temporary spike in traffic occurred: try again in a couple of minutes.</p>";
				} else if ( 505 === status ) {
					msg = "<p>505 (HTTP protocol not supported) - This message is extremely unlikely, so you may be using a non-standard browser.  Alternatively, your browser may have an incorrect setting, preventing it from using either HTTP v1 or v1.1.  Consider switching to a more mainstream browser (e.g. Chromium, Firefox, or Safari), or ask your local IT support for help.</p>";
				} else if ( 509 === status ) {
					msg = "<p>509 (bandwidth exceeded) - It appears that TemoaDB has gotten popular enough that this server has exceeded a bandwidth cap for this billing period.  If this error is not transient, please make sure we know about this via the <a href='https://groups.google.com/forum/#!forum/temoa-project' title='GoogleGroups forum'>Temoa Project forum</a>.</p>";
				} else if ( 511 === status ) {
					msg = "<p>511 (network authentication required) - This error most likely indicates a 'Captive Portal' situation: you may need to open a new browser tab or window and log on to a local network (e.g., agree to terms of service, pay money) before it will let you communicate with TemoaDB.</p>";
				} else if ( 522 === status ) {
					msg = "<p>522 (connection timed out) - TemoaDB's connection with your browser timed out.  This most likely means a lost couple of packets.  Resolution: try the action again.</p>";
				} else {
					msg = '<p>' + status + " - The server encountered a (currently undiagnosed) error.  If you can <strong>consistently</strong> recreate this error from a fresh reload (e.g., close and reopen the browser), then the Temoa Project developers would appreciate a bug report with the specifics.  Please file the bug on our <a href='https://github.com/hunteke/temoa/issues'>GitHub Issues</a> page.<p><p>Message from server: " + errorThrown + '</p>';
				}
			} else if ( status >= 400 ) {
				if ( 401 === status ) {
					msg = "<p>401 (unauthorized) - You are not currently known to the server.  This likely means that your session 'timed out' by not communicating with the server in an appropriate amount of time, or logged out in another tab or window (making this tab/window 'stale').  You will need to login again.";
				} else if ( 403 === status ) {
					msg = "<p>403 (forbidden) - Though the server recognizes you by the username '" + getCookie().username + "', the server does not recognize your authority to perform this action.  If you believe the action you took should be allowed (and thereby believe this message to be in error), please consider informing the Temoa Project via a <a href='https://github.com/hunteke/temoa/issues'>bug report.</a>  Note that unless you can provide exact instructions to recreate the issue, we may not be able to fix it.</p>"
				} else if ( 404 === status ) {
					msg = "<p>404 (not found) - The requested item could not be found.  Perhaps you need to reload the view in question?  If not, and you have discovered a <strong>recreatable</strong> error, please consider informing the Temoa Project via a <a href='https://github.com/hunteke/temoa/issues'>bug report.</a>  Note that unless there is an exact mechanism to recreate the issue, we may not be able to fix it.</p>";
				} else if ( 405 === status ) {
					msg = "<p>405 (method not allowed) - Your browser requested an action or resource through an incorrect mechanism.  This most likely indicates inconsitent logic in the Temoa web interface: if you can <em>consistently</em> recreate this message, please consider providing the Temoa Project with a <a href='https://github.com/hunteke/temoa/issues'>bug report.</a>  Note that unless there is an exact mechanism to recreate the issue, we may not be able to fix it.</p>";
				} else if ( 406 === status ) {
					msg = "<p>406 (not acceptable) - Your browser has told the server that it will only accept certain kinds of responses, none of which the server can produce.  This most likely indicates an incorrect setting or other issue with your browser.  You may ask for help on the <a href='https://groups.google.com/forum/#!forum/temoa-project' title='GoogleGroups forum'>Temoa Project forum</a>, but we will likely not be able to help.  Your local IT support may be of greater help.</p>";
				} else if ( 407 === status ) {
					msg = "<p>407 (unauthenticated proxy) - You are apparently accessing TemoaDB from through a proxy server.  This proxy server requires you to authenticate.  Generally, this means you will have to open a new tab or window and open a special organization-specific URL.  Your local IT support will be able to help as this error is not related to Temoa.</p>";
				} else if ( 408 === status ) {
					msg = "<p>408 (timeout) - The server was waiting for further information from your browser, but did not receive it in an appropriate amount of time.  This most likely means some packets were lost in transit (i.e., a fluke).  If you retry the action in question, it should succeed.</p>";
				} else if ( 410 === status ) {
					msg = "<p>410 (gone) - You or your browser requested some information from the server that no longer exists.  This likely means that you have an out-of-date version of the analysis.  If you reload this page (e.g., by closing and reopening your browser or force-reloading the page), this message should no longer appear.</p>";
				} else if ( 413 === status ) {
					msg = "<p>413 (too large) - You or your browser attempted to send too much data to the server.  As TemoaDB only deals with extremely small requests to the server (i.e., &lt;&lt; 512KiB), this is likely either an error with your browser or a bug within Temoa's web interface.  If you believe it to be the latter, please provide the Temoa Project with a <a href='https://github.com/hunteke/temoa/issues'>bug report.</a>  Note that unless there is an exact mechanism to recreate the issue, we may not be able to fix it.</p>";
				} else if ( 414 === status ) {
					msg = "<p>414 (request too long) - The request &ndash; what you would usually recognize as the URL in the white bar at the top of the browser window &ndash; for the request action was too long.  This request is not one that would see, but likely occurred when you selected a large number of items from a list.  Select a smaller number of items at a time to avoid this message.</p>";
				} else if ( 422 === status ) {
					return; // for form to handle
				} else if ( 429 === status ) {
					msg = "<p>429 (too many requests) - The server believes that you or your browser is asking for way too much information, and is therefore rate limiting your access.  To achieve this message, you would have to ask for an inordinate amount of information, such as what an automated program might be able to do.  This means you have scripted your access to TemoaDB (well done, but consider playing nice with our server), your browser has a bug, or you have found a bug within the Temoa web interface.  If you believe the latter, please consider creating a <a href='https://github.com/hunteke/temoa/issues'>bug report.</a>  Note that unless there is an exact mechanism to recreate the issue, we may not be able to fix it.</p>";
				} else {
					msg = '<p>' + status + " - There was a (currently undiagnosed) error with your browser's request to the server.  Consequently, the server has rejected the request.  If you can <strong>consistently</strong> recreate this error message from a fresh reload (e.g., close and reopen the browser), then the Temoa Project developers would appreciate a bug report with the specifics.  Please file the bug on our <a href='https://github.com/hunteke/temoa/issues'>GitHub Issues</a> page.<p><p>Message from server: " + errorThrown + '</p>';
				}
			}
			showStatus( null, null, msg );

		}
	});

	$('#ReloadLibs').click( function () { reloadLibs( false ); } );
	$(document).bind('keydown', 'ctrl+space', function () {
		reloadLibs( false );
	});

	$(document).bind('keydown', 'shift', function ( e ) {
		hideStatus();
		showStatus('Showing remove buttons ...', 'info');
		setTimeout( function ( ) { $('.remove').removeClass('hidden'); }, 1 );
	});
	$(document).bind('keyup', 'shift', function ( e ) {
		hideStatus();
		showStatus('Hiding remove buttons ...', 'info');
		setTimeout( function ( ) { $('.remove').addClass('hidden'); }, 1 );
	});

	updateAnalysisList();
}

$(document).ready( function () {
	BeginTemoaDBApp();
});

})();

console.log( 'TemoaLib loaded: ' + Date() );

