    /* STRICT 3-COLOR DOMINANT SYSTEM:
       1. Cobalt Blue:      #1E3BFF
       2. Acid Lime Green:  #C6FF00
       3. Obsidian Black:   #141519
       (+ White/Surface untuk kontras ruang baca)
    */
    tailwind.config = {
      theme: {
        extend: {
          fontFamily: {
            hero: ['Montserrat', 'sans-serif'],
            sans: ['Montserrat', 'sans-serif'],
            mono: ['Montserrat', 'monospace'],
            montserrat: ['Montserrat', 'sans-serif'],
          },
          colors: {
            cobalt: '#1E3BFF',
            acid: '#C6FF00',
            obsidian: '#0E1015',
            surface: '#F6F8FB',
            charcoal: '#171922',
            cardBg: '#12141C',
          }
        }
      }
    }
