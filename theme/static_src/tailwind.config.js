module.exports = {
    content: [
      // templates du thème
      "../templates/**/*.html",
      // templates globaux du projet
      "../../templates/**/*.html",
      // templates de l'app blog
      "../../blog/templates/**/*.html",
    ],
    theme: {
      extend: {},
    },
    plugins: [
      require("daisyui"), // uniquement si tu as choisi DaisyUI
    ],
  }
  