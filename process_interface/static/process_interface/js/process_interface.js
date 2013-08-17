var AA = null;
var AB = null;
var AC = null;

var COOKIE = 'TemoaDB_UISettings';

var original_user_list = null;
var original_analysis_list = null;

var logged_in = false;

var hoverEl = null;

var add_img       = '/static/process_interface/icons/blue_list_add.svg';
var remove_img    = '/static/process_interface/icons/red_list_remove.svg';

var tabularAttributes = {
  CostFixed:        createParameterTable( ['Period', 'Value'] ),
  CostVariable:     createParameterTable( ['Period', 'Value'] ),
  Efficiencies:     createParameterTable( ['Input', 'Output', 'Value'] ),
  EmissionActivity: createParameterTable( ['Pollutant', 'Input', 'Output', 'Value'] ),
  TechInputSplit:   createParameterTable( ['Input', 'Output', 'Fraction'] ),
  TechOutputSplit:  createParameterTable( ['Input', 'Output', 'Fraction'] )
};


var datalist = {
  'Efficiencies'     : { 'Input'  : null, 'Output' : null },
  'EmissionActivity' : { 'Pollutant': null, 'Input'  : null, 'Output' : null },
  'CostFixed'        : { 'Period' : null },
  'CostVariable'     : { 'Period' : null }
};


// Function borrowed from the Django Online documentation on CSRF:
// https://docs.djangoproject.com/en/dev/ref/contrib/csrf/
function csrfSafeMethod(method) {
	// these HTTP methods do not require CSRF protection
	return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}



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


function removeRowInputs ( $row ) {
	var inps = $row.find( 'td input' );
	for ( var i = 0; i < inps.length; ++i ) {
		var $el = $(inps[ i ]);
		var $parent = $($el.parent());
		$parent.empty();
		$parent.html( $el.val() );
	}
}


function showAddHideRemove ( el ) {
	var add_buttons    = null;
	var remove_buttons = null;
	if ( ! el ) {
		  // el === undefined or null both make this equate to true
		add_buttons    = $('img.add');
		remove_buttons = $('img.remove');
	} else {
		add_buttons    = $(el).find('img.add');
		remove_buttons = $(el).find('img.remove');
	}

	for ( var i = 0; i < add_buttons.length; ++i ) {
		$(add_buttons[i]).removeClass( 'hidden' );
	}
	for ( var i = 0; i < remove_buttons.length; ++i ) {
		$(remove_buttons[i]).addClass( 'hidden' );
	}

}

function hideAddShowRemove ( event ) {
	if ( null === hoverEl ) {
		return;
	}

	if ( event.keyCode === 17 ) {
		// 17 == "Control".  Seems only Firefox has .key property.  Sigh.
		var $target = $(hoverEl);
		var add_buttons = $target.find( 'img.add' );
		var remove_buttons = $target.find( 'img.remove' );

		for ( var i = 0; i < add_buttons.length; ++i ) {
			$(add_buttons[i]).addClass( 'hidden' );
		}
		for ( var i = 0; i < remove_buttons.length; ++i ) {
			$(remove_buttons[i]).removeClass( 'hidden' );
		}

	}
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
	var $status = $('#status');
	if ( ! cssclass ) { cssclass = 'error' }

	msg = escapeHTML( msg );

	$status.html( msg );
	$status.addClass( cssclass );
	$status.removeClass( 'hidden' );
	$status.clearQueue().stop(true, true).show().fadeIn( 1 ).delay( 1000 );

	// flash twice
	$status.fadeOut().fadeIn().delay( 1000 ).fadeOut().fadeIn();
	$status.delay( 1000 ).fadeOut( 4000 ).queue( hideStatus );
}


function deleteDataRow ( $row ) {
	AA = $row;
	console.log( AA );
	console.log( AA.data().rowid );
	var parameter = $row.data().parameter;
	var pId = $row.parents('form:first').data().processid;
	var aId = getCookie().selected_analysis['id'];

	var submit_url = '/analysis/' + aId + '/update/process/' + pId + '/delete/';
	submit_url += parameter;
	$.post( submit_url, {'rowid': $row.data().rowid } )
	.done( function ( response_data, textStatus, jqXHR ) {
		if ( $row.parent().children().length == 1 ) {
			console.log( 'Removing entire inner table');
			var $data = $(new Object());

			$row = $row.parents('tr:first');
			$row.empty()
			$data.attr( parameter, null );

			tabularAttributes[ parameter ]( $row, parameter, $data );
		} else {
			console.log( 'Removing single row:');
			console.log( $row );
			$row.remove();
		}
	})
	.fail( function ( jqXHR, textStatus, errorThrown ) {
		var server_msg = $( jqXHR ).attr( 'responseText' );
		showStatus( 'Unable to remove row in DB.  Server said: ' + server_msg );
	});

}


function submitUpdateParameter ( form ) {
	var $form = $(form);
	var inputs = $form.find('input.modifiable');

	if ( ! inputs.length ) {
		return;
	}

	var pId = $form.data().processid;
	var aId = getCookie().selected_analysis['id'];
	var $tRow = $(inputs[ 0 ]).parents('tr:first');
	var parameter = $tRow.data().parameter;
	var to_submit = {'parameter' : parameter};

	if ( $tRow.is('[data-rowid]') ) {
		to_submit['rowid'] = $tRow.data().rowid;
	}

	for ( var i = 0; i < inputs.length; ++i ) {
		var $tmp  = $(inputs[ i ]);
		var name  = $tmp.attr( 'name' );
		var val   = $tmp.val();

		val = $.trim( val );
		if ( ! val ) {
			console.log( 'Deleting!' );
			deleteData( $tRow );
			return false;
		}

		$tmp.attr('disabled', 'true');
		to_submit[ name ] = val;
	}

	var submit_url = '/analysis/' + aId + '/update/process/' + pId;
	$.post( submit_url, to_submit )
	.done( function ( response_data, textStatus, jqXHR ) {
		for ( var i = 0; i < inputs.length; ++i ) {
			var $tmp  = $(inputs[ i ]);
			$tmp.parent().removeClass( 'info' ).html( $tmp.val() );
		}

		if ( $tRow.is('[data-rowid]') ) {
			var rowId = JSON.parse( response_data );
			$tRow.attr('data-rowid', rowId );
			$tRow.data('rowid', rowId ); // b/c of unfortunate oversight in jQuery
		}

		// Success; give user visual acknowledgement of such
		hideStatus();
		$tRow.clearQueue().fadeOut().fadeIn();
	})
	.fail( function ( jqXHR, textStatus, errorThrown ) {
		var server_msg = $( jqXHR ).attr( 'responseText' );
		showStatus( 'Unable to alter process.  Server said: ' + server_msg );
		for ( var i = 0; i < inputs.length; ++i ) {
			var $tmp  = $(inputs[ i ]);
			$tmp.removeAttr('disabled');
		}
	});
	return false;
}



function writeParameterTable (
  $container, headers, remove_title, attr, value )
{
	  // "cTab" -> "cell table"
	var $cTab    = $('<table/>').addClass('innertable parameter');
	var $cHead   = $('<thead/>');
	var $cBody   = $('<tbody/>');
	var $caption = $('<caption/>');

	$container.append( $cTab );

	$cTab.append( $caption.html( attr ) );
	$cTab.append( $cHead );
	$cTab.append( $cBody );

	var $itcRow = $('<tr/>');  // "inner table cell row"
	var $img = $('<img/>');
	if ( logged_in ) {
		$img.attr({'src': add_img, 'title': 'Click to add new entry'} );
		$img.addClass( 'add clickable' );
		$img.click( function ( event ) {
			if ( $cTab.find('td input').length > 0 ) {
				// only allow one input row per parameter at a time.
				return;
			}

			var $newRow = $('<tr/>');
			var $newImg = $('<img/>');
			$newImg.attr({
			  'src' : remove_img,
			  'title' : 'Cancel',
			  'class' : 'hidden clickable remove'
			});
			$newImg.click( function ( event ) { deleteDataRow( $newRow ); });
			$newRow.attr({ 'data-parameter' : attr, 'data-rowid' : 'NewRow' });
			$newRow.append( $('<td/>').append( $newImg ));
			for ( var i in headers ) {
				var key = headers[ i ];
				var $newInput = $('<input />').attr({
				  'class'          : 'modifiable',
				  'type'           : 'text',
				  'name'           : key,
				});
				$newRow.append( $('<td/>').append( $newInput ));
			}
			$cBody.prepend( $newRow );
		});
		$itcRow.append( $('<th/>').append( $img ));
	}

	for ( var i in headers ) {
		$itcRow.append( $('<th/>').html( headers[ i ]));
	}
	$cHead.append( $itcRow );

	for ( var rowId in value ) {
		var rowData = value[ rowId ];
		$itcRow = $('<tr/>');
		$itcRow.attr({ 'data-rowid' : rowId, 'data-parameter' : attr });

		if ( logged_in ) {
			$img = $('<img />');
			$img.attr({'src': remove_img, 'title': remove_title} );
			$img.addClass( 'hidden remove clickable' );
			$img.click( function () {
				deleteDataRow( $(this).parents('tr:first') );
			});
			$itcRow.append( $('<td/>').append( $img ));

			$itcRow.dblclick( function ( ) {
				// this == <tr>
				var $thisRow = $(this);
				var $dataCells = $thisRow.find('.data');
				for ( var s1_i = 0; s1_i < $dataCells.length; ++s1_i ) {
					var $dCell = $($dataCells[ s1_i ]);
					var value  = $dCell.html();
					var $input = $('<input/>', {
					  'class'  : 'modifiable',
					  'name'   : headers[ s1_i ],
					  'value'  : value
					});
					$input.val( value );
					$dCell.empty().append( $input );
					$input.keydown( function ( e ) {
						if ( 27 == e.keyCode ) {
							for ( var s2_i = 0; s2_i < $dataCells.length; ++s2_i ) {
								var $cCell = $($dataCells[ s2_i ]); // "cancel" cell
								$cCell.html( $cCell.find('input').attr('value') );
							}
							$thisRow.effect('pulsate', { times:2 }, 1000);
						}
					});

				}
			});
		}

		for ( var sub_i in rowData ) {
			$cell = $('<td/>').addClass('data').html( rowData[ sub_i ] );
			$itcRow.append( $cell );
		}
		$cBody.append( $itcRow );
	}
	return false;
};

function createParameterTable ( headers ) {
	return function ( $tRow, attr, $pData ) {
		var remove_title = 'Remove row.';
		var value = $pData.attr( attr );
		var $cell = $('<td/>').attr('colspan', 2);
		$tRow.empty()

		$tRow.on('mouseenter', function() {
			hoverEl = this;
		});
		$tRow.on('mouseleave', function() {
			showAddHideRemove( this );
			if ( hoverEl === this ) {
				hoverEl = null;
			}
		});

		$cell.addClass( 'multiple_values' ).removeClass( 'info' );

		if ( ! value ) {
			if ( logged_in ) {
				var remove_title = 'Cancel adding row.';
				var value = { 'NewRow': new Array() };

				for ( var i in headers ) {
					var key = headers[ i ];
					var $newInput = $('<input />').attr({
					  'class' : 'modifiable',
					  'type'  : 'text',
					  'name'  : key,
					});
					value[ 'NewRow' ].push( $newInput );
				}


				var $img = $('<img />');
				$img.attr( {'src': add_img, 'title': 'No data; add new entry'} );
				$img.addClass( 'clickable' );
				$img.attr( 'tabindex', 0 );
				$img.click( function ( event ) {
					$tRow.empty().append($cell)
					writeParameterTable( $cell, headers, remove_title, attr, value );
				});
				$img.keypress( function ( e ) {
					if ( 13 === e.keyCode ) { // 13 == enter key
						$img.click();
					}
				});
				$tRow.append( $('<td/>').html( attr ) );
				$tRow.append( $('<td/>').append( $img ) );
			}

		} else {
			$tRow.append( $cell );
			writeParameterTable( $cell, headers, remove_title, attr, value );
		}
		return true;
	}
}


function createCheckbox ( is_enabled ) {
	return function ( $tRow, attr, $pData ) {
		var value = $pData.attr( attr );
		var checkbox = $('<input />');
		checkbox.attr({
		  'type'    : 'checkbox',
		  'checked' : value,
		  'class'   : 'modifiable'
		});

		$tRow.append( $('<td/>').html( attr ) );
		$tRow.append( $('<td/>').append( checkbox ) );

		return true;
	}
};


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

	  var select = original_user_list.clone();
	  $.each( options, function( val, text ) {
	    text = val + ' (' + text + ')';
	    select.append( $('<option/>').val( val ).html( text ));
	  });

	  $('#filter_analyses_username').replaceWith( select );
	  $userlist = $('#filter_analyses_username');
	  $userlist.change( selectUser );

	  var $cookie = getCookie();
	  if ( $cookie.selected_username ) {
	    $userlist.val( $cookie.selected_username );
	    $userlist.change();
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
	    var select = original_analysis_list.clone();
	    $.each( options, function( val, text ) {
	      select.append( $('<option/>').val( val ).html( text ));
	    });
	    $('#filter_analyses_analysis').replaceWith( select );
	    $('#filter_analyses_analysis').change( selectAnalysis );

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



function showTechnologyCharacteristics ( data ) {
	console.debug( 'Ignoring Tech Characteristics' );
	return;

	var booleanAttributes = {
	  Baseload: createCheckbox( true ),
	  Storage:  createCheckbox( true )
	}

	var specialAttributes = {}

	var techAttributes = [
	  'Description',
	  'Baseload',
	  'Storage',
	  'CapacityToActivity',
	  'GrowthRateMax',
	  'GrowthRateSeed',
	  'TechInputSplit',
	  'TechOutputSplit'
	];

	var css = ['even', 'odd'];

	var $techTable = $('#technology_characteristics .items')
	$techTable.empty()

	tData = $(data);

	var tId = tData.attr( 'TechnologyId' );

	var tName = tData.attr( 'Name' );
	var $block = $('<tbody/>', { 'data-technologyid' : tId });
	var $head = $('<tr/>');
	$head.append( $('<th/>', { colspan: 2 }).html( tName ) )
	$block.append( $head );

	var noRow = 0;

	$.each( techAttributes, function ( index, attr ) {
	  var $tr = $('<tr/>');
	  var $nameCell = $('<td/>').html( attr )
	  var newRow = false;

	  if ( attr in tabularAttributes ) {
	    newRow = tabularAttributes[ attr ]( $tr, attr, tData );
	  } else if ( attr in booleanAttributes ) {
	    newRow = booleanAttributes[ attr ]( $tr, attr, tData );
	  } else if ( attr in specialAttributes ) {
	    newRow = specialAttributes[ attr ]( $tr, attr, tData );
	  } else {
	    console.debug( '' + attr + ': ' + tData.attr( attr ) );
	    $tr.append( $('<td/>').html( attr ));
	    $tr.append( $('<td/>').html( tData.attr( attr )));
	    newRow = true;
	  }

	  if ( true === newRow ) {
	    noRow += 1
	    $tr.addClass( css[noRow % 2] );
	    $block.append( $tr );
	  }
	});

	$techTable.append( $block );

	$('#technology_characteristics').removeClass('hidden');
}


function showProcessCharacteristics ( data ) {
	var aId = getCookie().selected_analysis['id'];
	function existOrInvest ( must_be_new ) {
		return function ( $tRow, attr, $pData ) {
			$cookie = getCookie();
			period_0 = $cookie.selected_analysis['period_0'];
			if ( must_be_new === (period_0 > $pData.attr( 'Vintage' )) ) {
				return false;
			}

			var $cell = $('<td/>');
			var val = $pData.attr( attr );

			if ( null === val ) {
				$cell.addClass('info');
			}

			$tRow.attr( 'data-parameter', attr );
			$tRow.append( $('<td/>').html( attr ) );
			$tRow.append( $cell.html( val ) );

			if ( logged_in ) {
				var pId = $pData.attr( 'ProcessId' );
				var submit_url = '/analysis/'  + aId + '/update/process/' + pId;
				submit_url += '/' + attr;
				$cell.dblclick( function ( ) {
					// this == <td>
					var $thisCell = $(this);
					var $input = $('<input/>', {
					  'class'  : 'modifiable',
					  'name'   : 'value',
					});
					var value = $thisCell.html();
					var name = $thisCell.data().name
					$thisCell.empty();
					$thisCell.append( $input );

					$input.val( value );
					$input.focus();
					function cancel () {
						$thisCell.html( value );
						// flash to inform that the action was canceled
						$thisCell.effect('pulsate', { times:2 }, 1000)
					}
					$input.blur( cancel );
					$input.keydown( function ( e ) {
						if ( 27 === e.keyCode ) { cancel() }
					});
				});
			}

			return true;
		};
	}

	function isSetMember ( $tRow, attr, $pData ) {
		var is_member = $pData.attr( attr ) ? 'checkmark' : 'x_mark';

		$tRow.append( $('<td/>').html( attr ));
		$tRow.append( $('<td/>').addClass( is_member ));

		return true;
	}

	function hasDiscountRate ( $tRow, attr, $pData ) {
		var $cell = $('<td/>');
		var discrate = $pData.attr( attr );
		if ( null === discrate ) {
		  $cell.addClass('info');
		  discrate = getCookie().selected_analysis['global_discount_rate'];
		  discrate = '' + discrate + ' (GDR)';
		}

		if ( logged_in ) {
			var aId = getCookie().selected_analysis['id'];
			var pId = $pData.attr( 'ProcessId' );
			var submit_url = '/analysis/'  + aId + '/update/process/' + pId;
			submit_url += '/' + attr;

			$cell.editable({
			  closeOnEnter: true,
			  event: 'dblclick',
			  emptyMessage: discrate,
			  callback: function ( data ) {
			    if ( data.content ) {
			      data.$el.addClass( 'info' );
			      $.post( submit_url, {'value': data.content} )
			      .done( function ( response_data, textStatus, jqXHR ) {
			        data.$el.html( data.content );
			        data.$el.removeClass( 'info error' );
			        data.$el.clearQueue().fadeOut().fadeIn();
			      })
			      .fail( function ( jqXHR, textStatus, errorThrown ) {
			        data.$el.addClass( 'error' );
			        var server_msg = $( jqXHR ).attr( 'responseText' );
			        showStatus( 'Unable to update.  Server said: ' + server_msg );
			      })
			      .always( function ( ) {
			        data.$el.removeClass( 'info' );
			       });
			     }
			   }
			});
		}

		$tRow.append( $('<td/>').html( attr ) );
		$tRow.append( $cell.html( discrate ) );

		return true;
	}

	function getTechnologyInfo ( event ) {
			var $form = $(this).parents('form');
			var aId = getCookie().selected_analysis['id'];
			var pId = $form.attr( 'data-processid' );
			if ( ! pId ) {
				// Because we have sub tables, the pId may not be populated.  For
				// now, just ignore this.  I currently intend the workflow to be
				// "click on the process header.  (Currently visualized as the blue
				// bar.)
				return;
			}
			var get_url = '/analysis/' + aId +'/technology_info/' + pId;
			$.get( get_url )
			.done( function ( data ) {
				showTechnologyCharacteristics( data );
			})
			.fail( function ( jqXHR, textStatus, errorThrown ) {
				var server_msg = $( jqXHR ).attr( 'responseText' );
				showStatus( 'Unable to collect technology information from server.'
				  + '  Server said: ' + server_msg );
			});
		}

	  // The order here is the order of display in the process block
	var processAttributes = [
	  ['ExistingCapacity', existOrInvest( false ) ],
	  ['Baseload',         isSetMember ],
	  ['Storage',          isSetMember ],
	  ['Efficiencies',     createParameterTable( ['Input', 'Output', 'Value'] ) ],
	  ['EmissionActivity', createParameterTable( ['Pollutant', 'Input', 'Output', 'Value'] ) ],
	  ['CostInvest',       existOrInvest( true ) ],
	  ['CostFixed',        createParameterTable( ['Period', 'Value'] ) ],
	  ['CostVariable',     createParameterTable( ['Period', 'Value'] ) ],
	  ['DiscountRate',     hasDiscountRate ]
	];

	var css = ['even', 'odd'];

	// "process characteristic table"
	var $pcItems = $('#process_characteristics .items')
	$pcItems.empty();

	for ( var data_i in data ) {
		var $form  = $('<form/>');
		var $table = $('<table/>');
		var $tHead = $('<thead/>');
		var $tBody = $('<tbody/>');
		var $tRow  = $('<tr/>');

		var $pData = $(data[ data_i ]);
		var pId = $pData.attr( 'ProcessId' );
		console.debug( "Building Process Table.  pId: " + pId );
		var pName = $pData.attr( 'Technology' ) + ', ' + $pData.attr( 'Vintage' );

		  // hidden by css
		$form.append( $('<input />').attr({'type': 'submit'}));
		$form.attr({
		  'method'         : 'post',
		  'data-processid' : pId,    // lower case is apparently important
		  'data-parameter' : attr,    // lower case is apparently important
		  'onsubmit'       : 'return submitUpdateParameter( this );',
		});

		$tRow.append( $('<th/>', { 'colspan': 2 }).html( pName ) );
		$tHead.append( $tRow ).addClass( 'process_title' );
		$tHead.click( getTechnologyInfo );
		$table.append( $tHead ).addClass( 'process' );
		$table.append( $tBody );
		$form.append( $table );

		var noRow = 0;
		for ( var index in processAttributes ) {
			var attr = processAttributes[ index ][ 0 ];
			var func = processAttributes[ index ][ 1 ];
			$tRow = $('<tr/>');

			var newRow = func( $tRow, attr, $pData );

			if ( true === newRow ) {
				// There should be at least one row of attributes not added
				// Either ExistingCapacity or CostInvest
				noRow += 1
				$tRow.addClass( css[noRow % 2] );
				$tBody.append( $tRow );
			}
		}

		$pcItems.append( $form );
	}

	if ( data.length === 1 ) {
		var $form = $('#process_characteristics .items > form');
		var analysis_id = $('#filter_analyses_analysis').val();
		var process_id = $form.attr( 'data-processid' );

		$.get( '/analysis/' + aId +'/technology_info/' + pId )
		.done( function ( data ) {
			showTechnologyCharacteristics( data );
		})
		.fail( function ( jqXHR, textStatus, errorThrown ) {
			var server_msg = $( jqXHR ).attr( 'responseText' );
			showStatus( 'Unable to collect technology information from server.  '
			  + 'Server said: ' + server_msg );
		});

	}

	$('#process_characteristics').removeClass('hidden');
}

function showProcesses ( data ) {
	getProcessesInfo = function ( ) {
		// First, hide the process block to ensure that user is aware it's
		// changing
		$('#process_characteristics').addClass('hidden');

		var process_ids = new Array();
		var $selected = $('#processes .items tbody tr.ui-selected');
		$.each( $selected, function ( index, row ) {
		  process_ids.push( $( row ).attr('data-processid') );
		});
		if ( process_ids.length > 0 ) {
			process_ids.sort( function(lhs, rhs) { return lhs - rhs; });
			ids = process_ids.join(',');
			var analysis_id = $('#filter_analyses_analysis').val();
			$.ajax({
			  url: '/analysis/' + analysis_id + '/process_info/' + ids,
			  success: showProcessCharacteristics
			});

			// With the request out, set the cookie in case the page is reloaded
			var $current = getCookie();
			$current.selected_processes = process_ids;
			setCookie( $current );

			// Finally, hide the Tech characteristics to keep the two columns
			// in sync when they're displayed.
			$('#technology_characteristics').addClass('hidden');
		}
	};

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


function BeginTemoaDBApp ( ) {
	// create clone after onChange registration of event
	original_user_list     = $('#filter_analyses_username').clone();
	original_analysis_list = $('#filter_analyses_analysis').clone();

	if ( $('body').data().username ) {
		logged_in = true;
	}

	// Begin: Code adapted from Django documentation on CSRF
	var csrftoken = $('body').data().csrftoken;
	if ( typeof( csrftoken ) !== "undefined" ) {
		$.ajaxSetup({
		  crossDomain: false,  // There should be no need to talk elsewhere.
		  beforeSend: function ( xhr, settings ) {
		    if ( ! csrfSafeMethod( settings.type )) {
		      xhr.setRequestHeader( 'X-CSRFToken', csrftoken );
		    }
		  }
		});
	} else {
		var msg = 'There was an error with the a security token from the ';
		msg += 'server.  Consequently, you will not be able to update any ';
		msg += 'values, only browse the currently available data.  Please ';
		msg += 'contact the Temoa Project (via a GitHub ticket, or the forums) ';
		msg += 'if this is a problem for you.';
		alert( msg );
	}
	// End: borrowed code.

	$('body').keydown( hideAddShowRemove );
	$('body').keyup( function ( event ) { showAddHideRemove(); } );

	updateUserList();
	var $tech = $('#technology_characteristics')
	var left_of_tech = $tech.offset().left
	var top_of_tech = $tech.offset().top;
	top_of_tech -= parseFloat($tech.css('marginTop').replace(/auto/, 0));
	$(window).scroll( function () {
		var y = $(this).scrollTop();
		$tech = $('#technology_characteristics');
		if ( y > top_of_tech ) {
			$tech.addClass('fixed');
		} else {
			$tech.removeClass('fixed');
		}
	});
	console.debug( 'App has begun.');
}


$( document ).ready( BeginTemoaDBApp );
