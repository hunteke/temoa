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


Temoa.canControl.CommodityLists = can.Control('CommodityLists', {
	defaults: {
			view: Temoa.C.ROOT_URL + '/client_template/analysis_commodities.ejs'
		}
	},{
	init: function ( $el, options ) {
		var view = options.view;
		if ( Temoa.C.DEBUG )
			view += '?_=' + new Date().getTime();

		this.analysis = options.analysis;
		var analysis = this.analysis;  // needed for closure, below

		$el.html( can.view( view, {
			analysis: analysis,
			username: Temoa.fn.getCookie().username || null,
		}));

		$('#CommodityListsCloseButton').click( function ( ) {
			$('#ShowHideCommodityLists').click();
		});

		var username = Temoa.fn.getCookie().username;
		if ( ! (username && username === analysis.username ) )
			return;

		function select_start () {
			var $others = $(this).closest( 'form' ).find( 'tbody' ).not( this );
			$others.find('.ui-selected').removeClass( 'ui-selected' );
			$('#commodity_detail').fadeOut();
		}
		function select_stop () {
			var $info = $('#commodity_detail');

			var $sel = $( this ).find( 'tr.ui-selected' );
			var coms = new Array();
			for ( var i = 0; i < $sel.length; ++i ) {
				coms.push( $($sel[i]).data().commodity );
			}
			if ( ! (coms.length > 0) ) {
				return;
			}
			var username = Temoa.fn.getCookie().username || null;

			function createCommodityDetail ( toCreate ) {
				new CommodityDetail( $info, {
					analysis:  analysis,
					commodity: toCreate.shift(),
					username:  username
				});

				if ( toCreate.length > 0 ) {
					setTimeout( function () {
						createCommodityDetail( toCreate );
					}, 50 );  // 50 = something tiny; i.e., "reluinquish thread"
				}
			}

			$info.fadeOut( 'fast', function ( ) {
				// these steps are crucial: the Detail Controls are bound to the
				// $info element, so it must be removed for GC.  We then recreate
				// it, and accordingly set the closure variable ($info)
				var $newInfo = $('<div>', {id: 'commodity_detail'} );
				$newInfo.css('display', 'none');
				$info.replaceWith( $newInfo );
				$info = $newInfo.fadeIn();

				createCommodityDetail( coms );
			});
		};

		var $tables = $el.find('.items');

		var $tDemand   = $tables.filter('.demand').find('tbody');
		var $tEmission = $tables.filter('.emission').find('tbody');
		var $tPhysical = $tables.filter('.physical').find('tbody');

		$tDemand.selectable( {} );
		$tDemand.on( 'selectablestart', select_start );
		$tDemand.on( 'selectablestop', select_stop );
		$tEmission.selectable( {} );
		$tEmission.on( 'selectablestart', select_start );
		$tEmission.on( 'selectablestop', select_stop );
		$tPhysical.selectable( {} );
		$tPhysical.on( 'selectablestart', select_start );
		$tPhysical.on( 'selectablestop', select_stop );

	},
	create: function ( $el ) {
		var errors = {};
		var $form  = $el.closest('form');
		var $inputs = $form.find(':input');
		var data   = can.deparam( $form.serialize() );

		Temoa.fn.disable( $inputs );
		$form.find('.error').empty();  // remove any previous errors

		if ( Object.keys( errors ).length > 0 ) {
			// client-side checking for user convenience.  The server will check
			// for itself, of course.
			Temoa.fn.enable( $inputs );
			Temoa.fn.displayErrors( $form, errors );
			return;
		}

		this.analysis.attr( data ).save(
			function ( model ) {
				Temoa.fn.enable( $inputs );
				Temoa.fn.showStatus( 'Analysis successfully created.', 'info' );
		}, function ( xhr ) {
				Temoa.fn.enable( $inputs );
				if ( xhr && xhr.responseJSON ) {
					Temoa.fn.displayErrors( $form, xhr.responseJSON );
				}
		});
	},
	createNewCommodity: function ( CommodityObj, commodityOpts ) {
		var $newDiv = $('<div>', {id: 'commodity_detail'} );
		new CommodityDetail( $newDiv, {
			username: Temoa.fn.getCookie().username || null,
			analysis: this.analysis,
			commodity: new CommodityObj( commodityOpts )
		});
		$('#commodity_detail').replaceWith( $newDiv );
	},
	'#NewCommodityDemand click': function ( $el ) {
		var opts = {aId: this.analysis.id}
		this.createNewCommodity( CommodityDemand, opts );
	},
	'#NewCommodityEmission click': function ( $el ) {
		var opts = {aId: this.analysis.id, name: 'New Emission Commodity'}
		this.createNewCommodity( CommodityEmission, opts );
	},
	'#NewCommodityPhysical click': function ( $el ) {
		var opts = {aId: this.analysis.id, name: 'New Physical Commodity'}
		this.createNewCommodity( CommodityPhysical, opts );
	},
	'[name="CommodityDemandRemove"] click': function ( $el, ev ) {
		$el.closest( 'tr' ).data('commodity').destroy();
	},
	'[name="CommodityEmissionRemove"] click': function ( $el, ev ) {
		$el.closest( 'tr' ).data('commodity').destroy();
	},
	'[name="CommodityPhysicalRemove"] click': function ( $el, ev ) {
		$el.closest( 'tr' ).data('commodity').destroy();
	},
	'{CommodityDemand} created': function ( list, ev, commodity ) {
		this.analysis.commodity_demand.unshift( commodity.real_model );
	},
	'{CommodityEmission} created' : function ( list, ev, commodity ) {
		this.analysis.commodity_emission.unshift( commodity.real_model );
	},
	'{CommodityPhysical} created' : function ( list, ev, commodity ) {
		this.analysis.commodity_physical.unshift( commodity.real_model );
	},
});

})();

console.log( 'TemoaDB CommodityLists View loaded: ' + Date() );
