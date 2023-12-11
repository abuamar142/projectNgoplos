module.exports = {
  content: ["./templates/**/*.html"],
  theme: {
    extend: {
      colors: {
        primary: "#02A0FC",
        warning: "#FFB200",
        danger: "#FF3A29",
        success: "#34B53A",
      },
      backgroundImage: (theme) => ({
        gradient:
          "linear-gradient(130deg, #02A0FC 0%, rgba(255, 255, 255, 0.00) 72.9%)",
      }),
    },
  },
  plugins: [],
};
