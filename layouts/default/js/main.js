document.addEventListener("DOMContentLoaded", () => {
  const navigationToggle = document.querySelector(".mobile-nav-toggle");
  const sidebar = document.querySelector("#sidebar");

  if (navigationToggle && sidebar) {
    navigationToggle.addEventListener("click", () => {
      sidebar.classList.toggle("open");
    });
  }

  initializeCodeCopyButtons();

  const searchTriggers = document.querySelectorAll(".search-trigger");
  const searchOverlay = document.querySelector("#site-search");
  const searchInput = document.querySelector("#search-input");
  const searchClose = document.querySelector(".search-close");
  const searchStatus = document.querySelector("#search-status");
  const searchResults = document.querySelector("#search-results");
  const searchIndexPath = document.body.dataset.searchIndex;
  let searchIndexPromise;
  let searchOpener;

  if (!searchOverlay || !searchInput || !searchStatus || !searchResults || !searchIndexPath) {
    return;
  }

  const indexUrl = new URL(searchIndexPath, window.location.href);

  function loadSearchIndex() {
    if (!searchIndexPromise) {
      searchIndexPromise = fetch(indexUrl)
        .then((response) => {
          if (!response.ok) {
            throw new Error("Search index could not be loaded.");
          }
          return response.json();
        })
        .then((index) => {
          if (!Array.isArray(index)) {
            throw new Error("Search index is invalid.");
          }
          return index;
        });
    }
    return searchIndexPromise;
  }

  function setStatus(message) {
    searchStatus.textContent = message;
  }

  function queryTerms(query) {
    return query.trim().toLocaleLowerCase().split(/\s+/).filter(Boolean);
  }

  function snippet(content, terms) {
    const normalizedContent = content.toLocaleLowerCase();
    const matchAt = terms.reduce((firstMatch, term) => {
      const position = normalizedContent.indexOf(term);
      return position >= 0 && (firstMatch < 0 || position < firstMatch) ? position : firstMatch;
    }, -1);
    const start = Math.max(0, matchAt - 70);
    const end = Math.min(content.length, start + 180);
    return `${start > 0 ? "…" : ""}${content.slice(start, end)}${end < content.length ? "…" : ""}`;
  }

  function renderResults(results, terms) {
    searchResults.replaceChildren();
    const list = document.createElement("ul");
    list.className = "search-results-list";

    results.forEach((result) => {
      const item = document.createElement("li");
      const link = document.createElement("a");
      const excerpt = document.createElement("p");

      link.href = new URL(result.url, indexUrl).href;
      link.textContent = result.title;
      excerpt.textContent = snippet(result.content, terms);

      item.append(link, excerpt);
      list.append(item);
    });

    searchResults.append(list);
  }

  async function search(query) {
    const terms = queryTerms(query);
    searchResults.replaceChildren();

    if (!terms.length) {
      setStatus("Type one or more words to search.");
      return;
    }

    setStatus("Searching…");
    try {
      const index = await loadSearchIndex();
      if (searchInput.value !== query) {
        return;
      }

      const results = index
        .map((entry) => {
          const title = entry.title.toLocaleLowerCase();
          const content = entry.content.toLocaleLowerCase();
          const matches = terms.every((term) => title.includes(term) || content.includes(term));
          const titleMatches = terms.filter((term) => title.includes(term)).length;
          return { ...entry, matches, titleMatches };
        })
        .filter((entry) => entry.matches)
        .sort((first, second) => second.titleMatches - first.titleMatches || first.title.localeCompare(second.title))
        .slice(0, 10);

      if (!results.length) {
        setStatus("No matching pages found.");
        return;
      }

      setStatus(`${results.length} matching ${results.length === 1 ? "page" : "pages"}.`);
      renderResults(results, terms);
    } catch (error) {
      setStatus("Search is unavailable. Please try again later.");
    }
  }

  function openSearch(event) {
    searchOpener = event.currentTarget;
    searchOverlay.hidden = false;
    searchInput.focus();
  }

  function closeSearch() {
    searchOverlay.hidden = true;
    searchInput.value = "";
    searchResults.replaceChildren();
    setStatus("Type one or more words to search.");
    searchOpener?.focus();
  }

  function initializeCodeCopyButtons() {
    document.querySelectorAll(".article-content pre").forEach((pre) => {
      const highlightedContainer = pre.parentElement?.classList.contains("codehilite")
        ? pre.parentElement
        : null;
      const container = highlightedContainer || document.createElement("div");

      if (!highlightedContainer) {
        container.className = "code-block";
        pre.parentNode.insertBefore(container, pre);
        container.append(pre);
      } else {
        container.classList.add("code-block");
      }

      const copyButton = document.createElement("button");
      copyButton.type = "button";
      copyButton.className = "code-copy-button";
      copyButton.setAttribute("aria-label", "Copy code to clipboard");
      copyButton.title = "Copy code";
      copyButton.textContent = "📋";

      copyButton.addEventListener("click", async () => {
        const copied = await copyCode(pre.textContent);
        if (!copied) {
          copyButton.setAttribute("aria-label", "Unable to copy code");
          return;
        }

        copyButton.textContent = "✓";
        copyButton.setAttribute("aria-label", "Code copied to clipboard");
        copyButton.title = "Copied";
        window.setTimeout(() => {
          copyButton.textContent = "📋";
          copyButton.setAttribute("aria-label", "Copy code to clipboard");
          copyButton.title = "Copy code";
        }, 1600);
      });

      container.append(copyButton);
    });
  }

  async function copyCode(code) {
    try {
      if (navigator.clipboard?.writeText) {
        await navigator.clipboard.writeText(code);
        return true;
      }

      const textarea = document.createElement("textarea");
      textarea.value = code;
      textarea.setAttribute("readonly", "");
      textarea.style.position = "fixed";
      textarea.style.opacity = "0";
      document.body.append(textarea);
      textarea.select();
      const copied = document.execCommand("copy");
      textarea.remove();
      return copied;
    } catch (error) {
      return false;
    }
  }

  searchTriggers.forEach((trigger) => trigger.addEventListener("click", openSearch));
  searchClose?.addEventListener("click", closeSearch);
  searchOverlay.addEventListener("click", (event) => {
    if (event.target === searchOverlay) {
      closeSearch();
    }
  });
  searchInput.addEventListener("input", () => search(searchInput.value));
  document.addEventListener("keydown", (event) => {
    if (event.key === "Escape" && !searchOverlay.hidden) {
      closeSearch();
    }
  });
});
