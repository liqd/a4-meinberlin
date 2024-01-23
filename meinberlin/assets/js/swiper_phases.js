import Swiper from 'swiper'

// Needed due to issue with Swiper, issue link: https://github.com/import-js/eslint-plugin-import/issues/2266
/* eslint-disable import/no-unresolved */
import { Navigation, Pagination } from 'swiper/modules'
import 'swiper/css'
import 'swiper/css/navigation'
import 'swiper/css/pagination'
/* eslint-enable import/no-unresolved */

const createSwiper = ({ rootElement, options }) =>
  new Swiper(rootElement, options)

const initSwiper = () => {
  const config = {
    rootElement: '.swiper-container',
    options: {
      direction: 'horizontal',
      loop: true,
      modules: [Navigation, Pagination],
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
}

(function () {
  // Check if Swiper is already available globally
  const hasSwiper = typeof Swiper !== 'undefined'

  // Call swiper initialization if Swiper is available and swiper element found in DOM
  const hasSwiperContainer = document.querySelector('.swiper-container')

  if (hasSwiper && hasSwiperContainer) {
    initSwiper()
  }
})()
