<div dir="auto">

    <h1 class="break-text" id="bkmrk-page-title">{{$page->name}}</h1>

    <div style="clear:left;"></div>
    <div class="main-page-html-render" id="main-page-html-render">
        @if (isset($diff) && $diff)
            {!! $diff !!}
        @else
            {!! isset($page->renderedHTML) ? $page->renderedHTML : $page->html !!}
        @endif
    </div>
</div>