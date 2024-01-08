import Swiper from 'swiper/bundle'
import 'swiper/css/bundle'

const createSwiper = ({ rootElement, options }) =>
  new Swiper(rootElement, options)

const initSwiper = () => {
  const config = {
    rootElement: '.swiper-container',
    options: {
      direction: 'horizontal',
      loop: true,
      navigation: {
        nextEl: '.swiper-button-next',
        prevEl: '.swiper-button-prev'
      },
      pagination: {
        el: '.swiper-pagination',
        clickable: true,
        bulletElement: 'button',
        renderBullet: function (index, className) {
          return '<button class="' + className + '">' + (index + 1) + '</button>'
        }
      }
    }
  }

  createSwiper(config)
};

(function () {
  // Check if Swiper is already available globally
  const hasSwiper = typeof Swiper !== 'undefined'

  // Call swiper initialization if Swiper is available and swiper element found in DOM
  const hasSwiperContainer = document.querySelector('.swiper-container')

  if (hasSwiper && hasSwiperContainer) {
    initSwiper()
  }
})()
