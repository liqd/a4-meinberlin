document.addEventListener('DOMContentLoaded', function () {
  const timelineSteps = document.querySelectorAll('.timeline__step')
  const maxVisible = 5

  // Media query for desktop
  const isDesktop = () => window.matchMedia('(min-width: 768px)').matches

  function showAll () {
    timelineSteps.forEach(step => {
      step.style.display = 'flex'
    })
  }

  function setupNavigation () {
    let offsetIndex = 0
    const prevBtn = document.querySelector('.timeline__nav-btn--prev')
    const nextBtn = document.querySelector('.timeline__nav-btn--next')

    function updateVisibility () {
      timelineSteps.forEach((step, index) => {
        if (index >= offsetIndex && index < offsetIndex + maxVisible) {
          step.style.display = 'flex'
        } else {
          step.style.display = 'none'
        }
        step.classList.remove('is-last-visible')
        if (index === offsetIndex + maxVisible - 1 && step.style.display !== 'none') {
          step.classList.add('is-last-visible')
        }
      })
      if (prevBtn) prevBtn.disabled = offsetIndex === 0
      if (nextBtn) nextBtn.disabled = offsetIndex + maxVisible >= timelineSteps.length
    }

    if (nextBtn) {
      nextBtn.addEventListener('click', function () {
        if (offsetIndex + maxVisible < timelineSteps.length) {
          offsetIndex++
          updateVisibility()
        }
      })
    }
    if (prevBtn) {
      prevBtn.addEventListener('click', function () {
        if (offsetIndex > 0) {
          offsetIndex--
          updateVisibility()
        }
      })
    }
    updateVisibility()
  }

  function handleResize () {
    if (isDesktop() && timelineSteps.length > maxVisible) {
      setupNavigation()
    } else {
      showAll()
    }
  }

  // Check initially
  handleResize()
  // Check on window resize
  window.addEventListener('resize', handleResize)
})
