    function scrollBookshelf(event) {
        const bookshelf = event.currentTarget;
        bookshelf.scrollLeft += event.deltaY;
        event.preventDefault();
    }