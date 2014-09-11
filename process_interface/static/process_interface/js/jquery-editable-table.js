/*
 * The MIT License
 *
 * Copyright (c) 2013 Sauf Pompiers Ltd (MindMup)
 *
 * Permission is hereby granted, free of charge, to any person obtaining a copy of
 * this software and associated documentation files (the "Software"), to deal in
 * the Software without restriction, including without limitation the rights to
 * use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies
 * of the Software, and to permit persons to whom the Software is furnished to do
 * so, subject to the following conditions:
 *
 * The above copyright notice and this permission notice shall be included in all
 * copies or substantial portions of the Software.
 *
 * THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
 * IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
 * FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
 * AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
 * LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
 * OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
 * SOFTWARE.
 */

/* GitHub URL: https://github.com/mindmup/editable-table
 *  Using Git commit hash: 4bf7d6b04e4c54b0a606f27fe58e0689f590854e
 */

;(function ( $ ) {
$.fn.editableTableWidget = function (options) {
	'use strict';
	return $(this).each(function () {
		var buildDefaultOptions = function () {
			var opts = $.extend({}, $.fn.editableTableWidget.defaultOptions);
			opts.editor = opts.editor.clone();
			return opts;
		},
		activeOptions = $.extend(buildDefaultOptions(), options),
		ARROW_LEFT = 37, ARROW_UP = 38, ARROW_RIGHT = 39, ARROW_DOWN = 40, ENTER = 13, ESC = 27, TAB = 9,
		element = $(this),
		editor = activeOptions.editor.css('position', 'absolute').hide().appendTo(element.parent()),
		active,
		showEditor = function (select) {
			active = element.find('td:focus').not("[data-editable='false']");
			if (active.length) {
				editor.val(active.text())
					.removeClass('error')
					.show()
					.offset(active.offset())
					.css(active.css(activeOptions.cloneProperties))
					.width(active.width())
					.height(active.height())
					.focus();
				if (select) {
				editor.select();
				}
			}
		},
		setActiveText = function () {
			var text = editor.val(),
				evt = $.Event('change'),
				originalContent;
			if (active.text() === text || editor.hasClass('error')) {
				return true;
			}
			originalContent = active.html();
			active.text(text).trigger(evt, text);
			if (evt.result === false) {
				active.html(originalContent);
			}
		},
		movement = function (element, keycode) {
			if (keycode === ARROW_RIGHT) {
				return element.next('td');
			} else if (keycode === ARROW_LEFT) {
				return element.prev('td');
			} else if (keycode === ARROW_UP) {
				return element.parent().prev().children().eq(element.index());
			} else if (keycode === ARROW_DOWN) {
				return element.parent().next().children().eq(element.index());
			}
			return [];
		};
		editor.blur(function () {
			setActiveText();
			editor.hide();
		}).keydown(function (e) {
			if (e.which === ENTER) {
				setActiveText();
				editor.hide();
				active.focus();
				e.preventDefault();
				e.stopPropagation();
			} else if (e.which === ESC) {
				editor.val(active.text());
				e.preventDefault();
				e.stopPropagation();
				editor.hide();
				active.focus();
			} else if (e.which === TAB) {
				active.focus();
			} else if (this.selectionEnd - this.selectionStart === this.value.length) {
				var possibleMove = movement(active, e.which);
				if (possibleMove.length > 0) {
					possibleMove.focus();
					e.preventDefault();
					e.stopPropagation();
				}
			}
		})
		.on('input paste', function () {
			var evt = $.Event('validate');
			active.trigger(evt, editor.val());
			if (evt.result === false) {
				editor.addClass('error');
			} else {
				editor.removeClass('error');
			}
		});
		element.on('click keypress dblclick', showEditor)
		.css('cursor', 'pointer')
		.keydown(function (e) {
			var prevent = true,
				possibleMove = movement($(e.target), e.which);
			if (possibleMove.length > 0) {
				possibleMove.focus();
			} else if (e.which === ENTER) {
				showEditor(false);
			} else if (e.which === 17 || e.which === 91 || e.which === 93) {
				showEditor(true);
				prevent = false;
			} else {
				prevent = false;
			}
			if (prevent) {
				e.stopPropagation();
				e.preventDefault();
			}
		});

		element.find('td').not("[data-editable='false']").prop('tabindex', 1);

		$(window).on('resize', function () {
			if (editor.is(':visible')) {
				editor.offset(active.offset())
				.width(active.width())
				.height(active.height());
			}
		});
	});

};

$.fn.editableTableWidget.defaultOptions = {
	cloneProperties: ['padding', 'padding-top', 'padding-bottom', 'padding-left',
	  'padding-right', 'text-align', 'font', 'font-size', 'font-family',
	  'font-weight', 'border', 'border-top', 'border-bottom', 'border-left',
	  'border-right'],
	editor: $('<input>')
};

})( jQuery );
