/** @type {import('tailwindcss').Config} */
module.exports = {
    darkMode: ["class"],
    content: [
        "./jackgreen_co/core/templates/**/*.jinja.html",
        "./jackgreen_co/main/templates/main/**/*.jinja.html",
        "./jackgreen_co/blog/templates/blog/**/*.jinja.html",
        "./assets/js/**/*.js",
    ],
    theme: {
        container: {
            center: true,
            padding: "2rem",
            screens: {
                "2xl": "1400px",
            },
        },
        extend: {
            typography: {
                DEFAULT: {
                    css: {
                        color: "hsl(var(--muted-foreground))",
                        maxWidth: "none",
                        h1: {
                            color: "hsl(var(--foreground))",
                        },
                        h2: {
                            color: "hsl(var(--foreground))",
                        },
                        h3: {
                            color: "hsl(var(--foreground))",
                        },
                        h4: {
                            color: "hsl(var(--foreground))",
                        },
                        h5: {
                            color: "hsl(var(--foreground))",
                        },
                        h6: {
                            color: "hsl(var(--foreground))",
                        },
                        strong: {
                            color: "hsl(var(--muted-foreground))",
                        },
                        a: {
                            color: "hsl(var(--muted-foreground))",
                            fontWeight: "normal",
                            textDecoration: "underline",
                            textUnderlineOffset: "4px",
                            transitionProperty:
                                "color, background-color, border-color, text-decoration-color, fill, stroke",
                            transsitionTimingFunction: "cubic-bezier(0.4, 0, 0.2, 1)",
                            transitionDuration: "150ms",
                            "&:hover": {
                                color: "hsl(var(--foreground) / 0.8)",
                            },
                        },
                        ":where(ol > li)::marker": {
                            color: "hsl(var(--muted-foreground))",
                        },
                        pre: {
                            color: "hsl(var(--foreground))",
                            borderRadius: "var(--radius)",
                            backgroundColor: "hsl(var(--background))",
                            borderWidth: "1px",
                        },
                        li: {
                            marginTop: "0.2rem",
                            marginBottom: "0.2rem",
                        },
                        blockquote: {
                            color: "hsl(var(--muted-foreground))",
                            fontWeight: "normal",
                            borderLeftColor: "hsl(var(--foreground))",
                        },
                    },
                },
            },
            colors: {
                border: "hsl(var(--border))",
                input: "hsl(var(--input))",
                ring: "hsl(var(--ring))",
                background: "hsl(var(--background))",
                foreground: "hsl(var(--foreground))",
                primary: {
                    DEFAULT: "hsl(var(--primary))",
                    foreground: "hsl(var(--primary-foreground))",
                },
                secondary: {
                    DEFAULT: "hsl(var(--secondary))",
                    foreground: "hsl(var(--secondary-foreground))",
                },
                muted: {
                    DEFAULT: "hsl(var(--muted))",
                    foreground: "hsl(var(--muted-foreground))",
                },
                accent: {
                    DEFAULT: "hsl(var(--accent))",
                    foreground: "hsl(var(--accent-foreground))",
                },
                popover: {
                    DEFAULT: "hsl(var(--popover))",
                    foreground: "hsl(var(--popover-foreground))",
                },
                card: {
                    DEFAULT: "hsl(var(--card))",
                    foreground: "hsl(var(--card-foreground))",
                },
            },
            borderRadius: {
                lg: `var(--radius)`,
                md: `calc(var(--radius) - 2px)`,
                sm: "calc(var(--radius) - 4px)",
            },
            fontFamily: {
                sans: ["var(--font-sans)"],
            },
            keyframes: {
                "accordion-down": {
                    from: { height: "0" },
                    to: { height: "var(--radix-accordion-content-height)" },
                },
                "accordion-up": {
                    from: { height: "var(--radix-accordion-content-height)" },
                    to: { height: "0" },
                },
            },
            animation: {
                "accordion-down": "accordion-down 0.2s ease-out",
                "accordion-up": "accordion-up 0.2s ease-out",
            },
        },
    },
    plugins: [
        require("@tailwindcss/typography"),
    ],
};
