import math
class Pagination():
    def getPager(totalItems, currentPage = 1, pageSize = 10, pageview = 10):
        pages = []
        # calculate total pages
        totalPages = math.ceil(totalItems / pageSize);
        # ensure current page isn't out of range
        if (currentPage < 1): 
            currentPage = 1; 
        elif (currentPage > totalPages):
            currentPage = totalPages; 
        
        # startPage = 0, endPage = 0;
        if (totalPages <= pageview):
            # less than pageview (defauld =10) total pages so show all
            startPage = 1;
            endPage = totalPages;
        else: 
            # more than pageview (defauld =10) total pages so calculate start and end pages
            if (currentPage <= 6):
                startPage = 1;
                endPage = pageview;
            elif (currentPage + 4 >= totalPages):
                startPage = totalPages - 9;
                endPage = totalPages;
            else:
                startPage = currentPage - 5;
                endPage = currentPage + 4;
            # dddddddddddddddddddddddddddddd
            center_page = math.ceil(pageview / 2)
            if (currentPage <= center_page):
                startPage = 1;
                endPage = pageview;
            elif (currentPage + (center_page - 2) >= totalPages):
                startPage = totalPages - (pageview - 1);
                endPage = totalPages;
            else:
                startPage = currentPage - (pageview - (center_page - 2));
                endPage = currentPage + (center_page - 2);

        # calculate start and end item indexes
        startIndex = (currentPage - 1) * pageSize;
        endIndex = min(startIndex + pageSize - 1, totalItems - 1);

        # create an array of pages to ng-repeat in the pager control
        # pages = Array.from(Array((endPage + 1) - startPage).keys()).map(i => startPage + i);
        i=startPage
        while i <= endPage:
            pages.append({i:'?page='+ str(i)})
            i += 1
        # return object with all pager properties required by the view
        return {
            'totalItems': totalItems,
            'currentPage': currentPage,
            'pageSize': pageSize,
            'totalPages': totalPages,
            'startPage': startPage,
            'endPage': endPage,
            'startIndex': startIndex,
            'endIndex': endIndex,
            'pages': pages
        };
