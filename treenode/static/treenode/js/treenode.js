django.jQuery(function($){

    $(document).ready(function($)
    {
        var rowsExpandedDataKey = 'treenode_adminChangelistAccordionState';
        var rowsExpandedDataSep = '|';

        function init()
        {
            $('.treenode').each(function(){

                var scope = $(this);

                var rowPk = scope.attr('data-treenode');
                var rowAccordion = scope.attr('data-treenode-accordion');
                var rowDepth = scope.attr('data-treenode-depth');
                var rowLevel = scope.attr('data-treenode-level');
                var rowParentPk = scope.attr('data-treenode-parent');

                // add treenode attributes to row
                var rowEl = scope.closest('tr');
                rowEl.attr('data-treenode-accordion', rowAccordion);
                rowEl.attr('data-treenode-parent', rowParentPk);
                rowEl.attr('data-treenode-level', rowLevel);
                rowEl.attr('data-treenode-depth', rowDepth);
                rowEl.attr('data-treenode', rowPk);

                // remove original attributes
                scope.removeAttr('data-treenode');
                scope.removeAttr('data-treenode-accordion');
                scope.removeAttr('data-treenode-depth');
                scope.removeAttr('data-treenode-level');
                scope.removeAttr('data-treenode-parent');

                rowAccordion = Boolean(parseInt(rowAccordion));
                rowDepth = parseInt(rowDepth);

                rowEl.addClass('treenode-row');

                if (rowAccordion) {
                    rowEl.addClass('treenode-accordion');
                    if (rowDepth == 0) {
                        rowEl.addClass('treenode-no-depth');
                    }
                } else {
                    return;
                }

                rowEl.bind('treenode-expand', function(e){
                    e.preventDefault();
                    expandAccordionRow(rowEl);
                    return false;
                });

                rowEl.bind('treenode-collapse', function(e){
                    e.preventDefault();
                    collapseAccordionRow(rowEl);
                    return false;
                });

                // create accordion button and move level tabs before it
                var rowAnchor = scope.closest('a');

                var rowToggleButtonHTML = '';
                rowToggleButtonHTML += '<a class="treenode-accordion-button" href="#">';
                rowToggleButtonHTML += '<span class="vertical-line"></span>';
                rowToggleButtonHTML += '<span class="horizontal-line"></span>';
                rowToggleButtonHTML += '</a>';

                var rowToggleButtonEl = $(rowToggleButtonHTML);
                rowToggleButtonEl.css('margin-left', (25 * (rowLevel - 1)));
                rowToggleButtonEl.insertBefore(rowAnchor);
                rowToggleButtonEl.click(function(e){
                    e.preventDefault();
                    toggleAccordionRow(rowEl);
                    return false;
                });

                // on init hide row if it has a parent
                if (Boolean(rowParentPk)) {
                    rowEl.addClass('treenode-hide');
                }
            });
        }

        function toggleAccordionRow(target)
        {
            if (target.hasClass('treenode-accordion')) {
                if (target.hasClass('treenode-expanded')) {
                    target.removeClass('treenode-expanded');
                    target.trigger('treenode-collapse');
                } else {
                    target.addClass('treenode-expanded');
                    target.trigger('treenode-expand');
                }

                updateAccordionEvenOddRows();
                saveAccordionExpandedRows();
            }
        }

        function expandAccordionRow(target)
        {
            var rowPk = target.attr('data-treenode');
            var rowSel = '[data-treenode-parent="' + rowPk + '"]';
            var rowEl = $('.treenode-accordion').filter(rowSel);
            if (!target.hasClass('treenode-hide')) {
                rowEl.removeClass('treenode-hide');
            }
            rowEl.each(function(){
                if ($(this).hasClass('treenode-expanded')) {
                    $(this).trigger('treenode-expand');
                }
            });
        }

        function collapseAccordionRow(target)
        {
            var rowPk = target.attr('data-treenode');
            var rowSel = '[data-treenode-parent="' + rowPk + '"]';
            var rowEl = $('.treenode-accordion').filter(rowSel);
            rowEl.addClass('treenode-hide');
            rowEl.trigger('treenode-collapse');
        }

        function updateAccordionEvenOddRows()
        {
            $('.treenode-accordion').not('.treenode-hide').each(function(index, element){
                $(this).removeClass('row1')
                $(this).removeClass('row2');
                // update rows even/odd class
                if ((index % 2) == 0) {
                    $(this).addClass('row1');
                } else {
                    $(this).addClass('row2');
                }
            });
        }

        function loadAccordionExpandedRows()
        {
            // TODO: add option to expand all on load
            var rowEl;
            var rowSel;
            var rowsExpandedData = (localStorage.getItem(rowsExpandedDataKey) || '');
            var rowsExpanded = rowsExpandedData.split(rowsExpandedDataSep);
            for (var i = 0, j = rowsExpanded.length; i < j; i++) {
                rowSel = '.treenode-accordion[data-treenode="' + rowsExpanded[i] + '"]';
                rowEl = $(rowSel);
                rowEl.addClass('treenode-expanded');
                rowEl.trigger('treenode-expand');
            }
        }

        function saveAccordionExpandedRows()
        {
            var rowPk;
            var rowsExpanded = [];
            $('.treenode-accordion.treenode-expanded').each(function(){
                rowPk = $(this).attr('data-treenode');
                rowsExpanded.push(rowPk);
            });
            var rowsExpandedData = rowsExpanded.join(rowsExpandedDataSep);
            localStorage.setItem(rowsExpandedDataKey, rowsExpandedData);
        }

        init();
        loadAccordionExpandedRows();
        updateAccordionEvenOddRows();
        saveAccordionExpandedRows();
    });
});