export default function (eleventyConfig) {
  // Copy static assets straight through to the built site
  eleventyConfig.addPassthroughCopy("src/assets");
  eleventyConfig.addPassthroughCopy("src/admin");
  eleventyConfig.addPassthroughCopy("src/CNAME");

  // --- Collections -----------------------------------------------------
  // Each of these reads the Markdown files in src/content/<folder>/.
  // The CMS writes to exactly these folders, so anything a collaborator
  // adds through the admin panel appears here automatically.

  eleventyConfig.addCollection("news", (collection) =>
    collection
      .getFilteredByGlob("src/content/news/*.md")
      .sort((a, b) => b.data.date - a.data.date)
  );

  eleventyConfig.addCollection("events", (collection) =>
    collection
      .getFilteredByGlob("src/content/events/*.md")
      .sort((a, b) => a.data.date - b.data.date)
  );

  eleventyConfig.addCollection("people", (collection) =>
    collection
      .getFilteredByGlob("src/content/people/*.md")
      .sort((a, b) => (a.data.order || 99) - (b.data.order || 99))
  );

  // --- Filters ---------------------------------------------------------

  const MONTHS = [
    "January", "February", "March", "April", "May", "June",
    "July", "August", "September", "October", "November", "December",
  ];

  // 14 March 2026
  eleventyConfig.addFilter("longDate", (value) => {
    const d = new Date(value);
    return `${d.getUTCDate()} ${MONTHS[d.getUTCMonth()]} ${d.getUTCFullYear()}`;
  });

  // 2026-03-14 (for <time datetime="">)
  eleventyConfig.addFilter("isoDate", (value) =>
    new Date(value).toISOString().split("T")[0]
  );

  eleventyConfig.addFilter("year", (value) => new Date(value).getUTCFullYear());

  eleventyConfig.addFilter("limit", (array, n) => array.slice(0, n));

  // Select collection items whose front-matter field equals a value
  eleventyConfig.addFilter("where", (array, key, value) =>
    array.filter((item) => item.data[key] === value)
  );

  // Is this event still in the future?
  eleventyConfig.addFilter("upcoming", (events) => {
    const now = new Date();
    now.setHours(0, 0, 0, 0);
    return events.filter((e) => new Date(e.data.date) >= now);
  });

  eleventyConfig.addFilter("past", (events) => {
    const now = new Date();
    now.setHours(0, 0, 0, 0);
    return events.filter((e) => new Date(e.data.date) < now).reverse();
  });

  return {
    dir: {
      input: "src",
      output: "_site",
      includes: "_includes",
      data: "_data",
    },
    markdownTemplateEngine: "njk",
    htmlTemplateEngine: "njk",
  };
}
