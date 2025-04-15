<style>
    .modern-sidebar {
        margin-top: 10px;
        /* background-color: #ffffff; Light background for the sidebar */
        border-radius: 8px; Rounded corners for the sidebar
        /* margin: 2px; */
        /* padding: 5px; */
        font-family: sans-serif;
        color: #333;
        overflow-y: auto; /* Enable scrolling for long trees */
        -webkit-user-select: none; /* Prevent text selection during drag/interaction */
        user-select: none;
    }

    .tree-list {
        list-style-type: none;
        padding: 0px;
        margin: 0;
        list-style: none;
    }

    .tree-item {
        position: relative;
    }

    .tree-header {
        justify-content: center; 
        align-items: center; 
        display: flex;
        align-content: center;
        gap: 8px;
        padding: 5px 10px;
        cursor: pointer;
    }

    .tree-header:hover {
        background-color: #e9ecef;
    }

    .item-name {
        flex-grow: 1;
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis; 
    }

    .tree-children {
        list-style-type: none;
        padding: 0px;
        padding-left: 2px;
        display: none; /* Initially hide children */
    }

    .tree-item.open > .tree-children {
        display: block;
    }

    .tree-leaf-link {
        display: flex;
        align-items: center;
        gap: 8px;
        padding: 8px 16px;
        text-decoration: none;
        color: inherit;
    }

    .tree-leaf-link:hover {
        background-color: #e9ecef;
    }

    .tree-leaf-link.active {
        font-weight: bold;
        color: #007bff;
    }

    /* Level-based indentation using data attributes for more flexibility */
    [data-level="1"] > .tree-header,
    [data-level="1"] > .tree-leaf-link {
        padding-left: 4px;
    }

    [data-level="2"] > .tree-header,
    [data-level="2"] > .tree-leaf-link {
        padding-left: 12px;
    }

    [data-level="3"] > .tree-header,
    [data-level="3"] > .tree-leaf-link {
        padding-left: 18px;
    }

    [data-level="4"] > .tree-header,
    [data-level="4"] > .tree-leaf-link {
        padding-left: 28px;
    }


    .item-icon-wrapper {
        display: flex;
        align-items: center;
        justify-content: center;
        width: 20px;
        height: 20px;
        border-radius: 50%;
        background-color: color-mix(in srgb, currentColor 20%, white); /* Lighter shade of currentColor */
    }

    .tree-header-icon {
        font-size: 24px;
        color: currentColor; /* Uses the same as text color */
    }

    /* Add more levels as needed */
</style>

<nav id="book-tree" class="book-tree modern-sidebar" aria-label="{{ trans('entities.books_navigation') }}" >
    <h5>Books Tree, Select from direct Directory</h5>
    <ul class="tree-list">
        @foreach ($sidebarTree as $shelf)
            {{-- Shelves --}}
            <li class="tree-item folder {{ $shelf->is_open ? 'open' : '' }}" data-level="1">
                <div class="tree-header text-bookshelf icon-list-item outline-hover">
                    <span class="tree-header-icon">@icon('bookshelf')</span>
                    <span class="item-content-name">{{ $shelf->name }}</span>
                </div>
                <ul class="tree-children">
                    {{-- Books --}}
                    @foreach ($shelf->books as $book)
                        <li class="tree-item folder {{ $book->is_open ? 'open' : '' }}" data-level="2">
                            <div class="tree-header text-book icon-list-item outline-hover">
                                <span class="tree-header-icon">@icon('book')</span>
                                <span class="item-content-name">{{ $book->name }}</span>
                            </div>
                            <ul class="tree-children">
                                {{-- Lone Pages --}}
                                {{-- @foreach ($book->pages as $page)
                                    <li class="tree-item file text-page" data-level="4">
                                        <a href="{{ $page->getUrl() }}" class="tree-leaf-link  icon-list-item outline-hover {{ isset($current) && $current->id === $page->id ? '' : '' }}">
                                            <span class="tree-header-icon">@icon('page')</span>
                                            <span class="item-content-name">{{ $page->name }}</span>
                                        </a>
                                    </li>
                                @endforeach --}}

                                {{-- Chapters --}}
                                @foreach ($book->chapters as $chapter)
                                    <li class="tree-item folder {{ $chapter->is_open ? 'open' : '' }}" data-level="3">
                                        <div class="tree-header text-chapter icon-list-item outline-hover">
                                            <span class="tree-header-icon">@icon('chapter')</span>
                                            <span class="item-content-name">{{ $chapter->name }}</span>
                                        </div>
                                        
                                        <ul class="tree-children">
                                            @foreach ($chapter->pages as $page)
                                                <li class="tree-item file text-page" data-level="4">
                                                    <a href="{{ $page->getUrl() }}" class="tree-leaf-link  icon-list-item outline-hover {{ isset($current) && $current->id === $page->id ? '' : '' }}">
                                                        <span class="tree-header-icon">@icon('page')</span>
                                                        <span class="item-content-name">{{ $page->name }}</span>
                                                    </a>
                                                </li>
                                            @endforeach
                                        </ul>
                                    </li>
                                @endforeach
                            </ul>
                        </li>
                    @endforeach
                </ul>
            </li>
        @endforeach
    </ul>
</nav>
