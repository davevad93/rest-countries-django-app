// Class to manage search input, suggestions dropdown, and country cards.
class CountrySearch {
    constructor() {
        this.searchInput = document.querySelector("#id_search_term"); // Search input field
        this.searchDropdown = document.querySelector("#search-dropdown"); // Suggestions dropdown
        this.activeSearchItem = -1; // Index of active search suggestion
        this.init(); // Initialize functionality
    }

    // Initialize search input and dropdown
    init() {
        document.addEventListener("DOMContentLoaded", () => {
            this.handleSearchTerm(); // Handle search term //Preferred DOMContentLoaded for better performance and compatibility
            this.searchInput.addEventListener("input", this.handleSearchInputChange.bind(this)); // Listen for input changes
            this.searchInput.addEventListener("keydown", this.handleSearchInputKeyDown.bind(this)); // Listen for keydown events
        };
        this.attachCardEventListeners(); // Attach event listeners to country cards
    }

    // Handle keydown event on search input
    handleSearchInputKeyDown(event) {
        const items = Array.from(this.searchDropdown.children); // Convert dropdown children to array
        if (items.length === 0) return; // Return if no suggestions
        if (event.key === 'Escape') {  
            this.clearSearchDropdown(); //Use Escape key to close suggestions //new 
            this.searchInput.blur();
        }
        if (event.key === 'ArrowDown' || event.key === 'ArrowUp') {
            this.handleArrowKeys(event, items); // Handle arrow key navigation
        } else if (event.key === 'Enter') {
            this.handleEnterKey(items); // Handle enter key selection
        }
    }

    // Handle arrow key press for suggestion selection
    handleArrowKeys(event, items) {
        event.preventDefault(); // Prevent default behavior
        this.removeActiveClass(items); // Remove active class from suggestions
        this.activeSearchItem = event.key === 'ArrowDown'
            ? (this.activeSearchItem + 1) % items.length // Move down
            : (this.activeSearchItem - 1 + items.length) % items.length; // Move up

        items[this.activeSearchItem].classList.add('active'); // Add active class to selected suggestion
    }

    // Handle enter key press for suggestion selection
    handleEnterKey(items) {
        if (this.activeSearchItem === -1) return; // Return if no active suggestion
        const activeItem = items[this.activeSearchItem]; // Get active suggestion
        this.searchInput.value = activeItem.textContent; // Set input value to suggestion
        this.clearSearchDropdown(); // Clear suggestions dropdown
        this.redirectToSearch(activeItem.textContent); // Redirect to search page
        this.handleSearchTerm(activeItem.textContent); // Handle search term
        this.activeSearchItem = -1; // Reset active suggestion
    }

    // Handle search term on page load or input change
    handleSearchTerm(searchTerm = null) {
        if (!searchTerm) {
            const urlParams = new URLSearchParams(window.location.search); // Get URL parameters
            searchTerm = urlParams.get('search_term'); // Get search term from URL
        }

        if (searchTerm) {
            this.handleSearchedCountry(searchTerm); // Handle searched country
        }
        if (!searchTerm) this.handleSearchInputChange(); // Handle input change if no search term
    }

    // Handle search input change event
    handleSearchInputChange() {
        const searchValue = this.searchInput.value.trim(); // Get trimmed input value
        searchValue ? this.fetchSearchSuggestions(searchValue) : this.clearSearchDropdown(); // Fetch suggestions or clear dropdown
    }

    // Fetch search suggestions from server
    fetchSearchSuggestions(searchValue) {
        fetch(`/search_countries/?search_term=${encodeURIComponent(searchValue)}&autocomplete=true`)
            .then((response) => response.json())
            .then((data) => this.updateSuggestionsDropdown(data.suggestions)); // Update dropdown with suggestions
    }

    // Update dropdown with search suggestions
    updateSuggestionsDropdown(suggestions) {
        this.clearSearchDropdown(); // Clear dropdown
        suggestions.forEach((suggestion) => {
            const listItem = this.createListItem(suggestion); // Create list item for suggestion
            this.searchDropdown.appendChild(listItem); // Append suggestion to dropdown
        });
        this.searchDropdown.style.display = 'block'; // Display dropdown
    }

    // Create list item for search dropdown
    createListItem(suggestion) {
        const listItem = document.createElement('li'); // Create list item
        listItem.textContent = suggestion; // Set text content
        listItem.classList.add('search-item'); // Add class
        listItem.addEventListener('click', () => this.redirectToSearch(suggestion)); // Add click event listener
        return listItem;
    }

    // Clear dropdown on click outside
    clearDropdownOnClick() {
        document.addEventListener('click', (event) => {
            const isClickInsideDropdown = this.searchDropdown.contains(event.target); // Check if click is inside dropdown
            if (!isClickInsideDropdown) {
                this.searchDropdown.innerHTML = ''; // Clear dropdown
                this.searchDropdown.style.display = 'none'; // Hide dropdown
            }
        });
    }

    // Clear search dropdown
    clearSearchDropdown() {
        this.searchDropdown.innerHTML = ''; // Clear dropdown
        this.searchDropdown.style.display = 'none'; // Hide dropdown
        this.clearDropdownOnClick(); // Clear dropdown on click outside
    }

    // Attach event listeners to country cards
    attachCardEventListeners() {
        // Check page location to avoid attaching listeners on search page
        if (window.location.pathname !== '/search_countries/') {
            const countryCards = document.querySelectorAll("#country-card"); // Get country cards
            countryCards.forEach((countryCard) => {
                countryCard.addEventListener('click', () => {
                    const countryName = countryCard.querySelector('#country-name').textContent; // Get country name
                    if (this.searchInput.value.trim() !== countryName) {
                        this.redirectToSearch(countryName); // Redirect to search if country name doesn't match input
                    }
                });
            });
        }
    }

    // Handle searched country and disable pointer events on page load
    handleSearchedCountry(searchTerm) {
        const countryCards = document.querySelectorAll('#country-card'); // Get country cards
        countryCards.forEach((card) => {
            const countryName = card.querySelector('#country-name').textContent; // Get country name
            if (countryName.toLowerCase() === searchTerm.toLowerCase()) {
                card.classList.add('searched'); // Add class to indicate searched country
            }
        });
    }

    // Remove active class from search suggestion items
    removeActiveClass(items) {
        if (this.activeSearchItem >= 0 && this.activeSearchItem < items.length) {
            items[this.activeSearchItem].classList.remove('active'); // Remove active class
        }
    }

    // Redirect to search page
    redirectToSearch(searchTerm) {
        window.location.href = `/search_countries/?search_term=${encodeURIComponent(searchTerm)}`; // Redirect with search term
    }
}

// Class to manage region select form
class RegionSelect {
    constructor(countrySearch) {
        this.regionSelect = document.querySelector("#id_regions"); // Region select element
        this.countryContainer = document.querySelector("#country-container"); // Country container
        this.countrySearch = countrySearch; // CountrySearch instance
        if (this.regionSelect && this.countryContainer) {
            this.init(); // Initialize functionality
        }
    }

    // Initialize the region select.
    init() {
        if (this.regionSelect) { 
            this.regionSelect.addEventListener("change", () => this.handleRegionSelectChange()); // Add event listener for 'change' event to handle region selection changes
        }
    }

    // Fetch countries by region from the server
    fetchCountriesByRegion(region) {
        this.countryContainer.innerHTML = ''; // Clear country container
        fetch(`/filter_regions/?region=${region}`)
            .then((response) => response.json())
            .then((data) => {
                this.countryContainer.innerHTML = data.data; // Update country container with fetched data
                this.countrySearch.attachCardEventListeners(); // Attach event listeners to updated country cards
            });
    }

    // Handle region select change event
    handleRegionSelectChange() {
        const selectedRegion = this.regionSelect.value; // Get selected region
        this.fetchCountriesByRegion(selectedRegion); // Fetch countries for selected region
    }
}

// Initialize the CountrySearch and RegionSelect classes when DOM content is loaded
document.addEventListener("DOMContentLoaded", function () {
    const countrySearch = new CountrySearch(); // Initialize CountrySearch
    if (countrySearch) {
        return new RegionSelect(countrySearch); // Initialize RegionSelect with CountrySearch instance
    }
});
