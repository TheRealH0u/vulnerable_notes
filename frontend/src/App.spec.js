import { describe, it, expect, vi } from 'vitest'
import { mount } from '@vue/test-utils'
import App from './App.vue'

// Mock axios
vi.mock('axios', () => ({
  default: {
    post: vi.fn(),
    get: vi.fn()
  }
}))

describe('App Component', () => {
  it('renders app div', () => {
    const wrapper = mount(App, {
      global: {
        stubs: {
          'router-view': true,
          'router-link': true
        },
        mocks: {
          $router: {
            push: vi.fn()
          },
          $route: {
            path: '/'
          }
        }
      }
    })
    expect(wrapper.find('div').exists()).toBe(true)
  })

  it('initializes with null user', () => {
    const wrapper = mount(App, {
      global: {
        stubs: {
          'router-view': true,
          'router-link': true
        },
        mocks: {
          $router: { push: vi.fn() },
          $route: { path: '/' }
        }
      }
    })
    expect(wrapper.vm.user).toBeNull()
  })

  it('has fetchUser method', () => {
    const wrapper = mount(App, {
      global: {
        stubs: {
          'router-view': true,
          'router-link': true
        },
        mocks: {
          $router: { push: vi.fn() },
          $route: { path: '/' }
        }
      }
    })
    expect(typeof wrapper.vm.fetchUser).toBe('function')
  })

  it('has doLogout method', () => {
    const wrapper = mount(App, {
      global: {
        stubs: {
          'router-view': true,
          'router-link': true
        },
        mocks: {
          $router: { push: vi.fn() },
          $route: { path: '/' }
        }
      }
    })
    expect(typeof wrapper.vm.doLogout).toBe('function')
  })
})
