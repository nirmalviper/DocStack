import {Component} from './component';

export class TriLayout extends Component {

    setup() {
        this.container = this.$refs.container;
        this.tabs = this.$manyRefs.tab;

        this.lastLayoutType = 'none';
        this.onDestroy = null;
        this.scrollCache = {
            content: 0,
            info: 0,
        };
        this.lastTabShown = 'content';

        // Bind any listeners
        this.mobileTabClick = this.mobileTabClick.bind(this);

        // Watch layout changes
        this.updateLayout();
        window.addEventListener('resize', () => {
            this.updateLayout();
        }, {passive: true});
    }

    updateLayout() {
        // Force the layout to behave like mobile for all screen sizes
        const newLayout = 'mobile';
        if (newLayout === this.lastLayoutType) return;

        if (this.onDestroy) {
            this.onDestroy();
            this.onDestroy = null;
        }

        this.setupMobile(); // Always use the mobile setup

        this.lastLayoutType = newLayout;
    }

    setupMobile() {
        for (const tab of this.tabs) {
            tab.addEventListener('click', this.mobileTabClick);
        }

        this.onDestroy = () => {
            for (const tab of this.tabs) {
                tab.removeEventListener('click', this.mobileTabClick);
            }
        };

        // Ensure the container has the mobile class for styling
        this.container.classList.add('mobile-layout');
    }

    /**
     * Action to run when the mobile info toggle bar is clicked/tapped
     * @param event
     */
    mobileTabClick(event) {
        const {tab} = event.target.dataset;
        this.showTab(tab);
    }

    /**
     * Show the content tab.
     * Used by the page-display component.
     */
    showContent() {
        this.showTab('content', false);
    }

    /**
     * Show the given tab
     * @param {String} tabName
     * @param {Boolean }scroll
     */
    showTab(tabName, scroll = true) {
        this.scrollCache[this.lastTabShown] = document.documentElement.scrollTop;

        // Set tab status
        for (const tab of this.tabs) {
            const isActive = (tab.dataset.tab === tabName);
            tab.setAttribute('aria-selected', isActive ? 'true' : 'false');
        }

        // Toggle section
        const showInfo = (tabName === 'info');
        this.container.classList.toggle('show-info', showInfo);

        // Set the scroll position from cache
        if (scroll) {
            const pageHeader = document.querySelector('header');
            const defaultScrollTop = pageHeader.getBoundingClientRect().bottom;
            document.documentElement.scrollTop = this.scrollCache[tabName] || defaultScrollTop;
            setTimeout(() => {
                document.documentElement.scrollTop = this.scrollCache[tabName] || defaultScrollTop;
            }, 50);
        }

        this.lastTabShown = tabName;
    }
    
}
