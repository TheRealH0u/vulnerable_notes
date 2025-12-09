import { describe, it, expect, vi } from 'vitest'
import { mount } from '@vue/test-utils'
import App from './App.vue'

// Mock axios - IMPORTANT: must return Promise
const mockAxios = {
  get: vi.fn(() => Promise.resolve({ data: { username: null } })),
  post: vi.fn(() => Promise.resolve({ data: { message: 'ok' } }))
}

vi.mock('axios', () => ({
  default: mockAxios
}))

describe('App Component', () => {
  it('renders app div', async () => {
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
    await wrapper.vm.$nextTick()
    expect(wrapper.find('div').exists()).toBe(true)
  })

  it('initializes with null user', async () => {
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
    await wrapper.vm.$nextTick()
    expect(wrapper.vm.user).toBeNull()
  })

  it('has fetchUser method', async () => {
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
    await wrapper.vm.$nextTick()
    expect(typeof wrapper.vm.fetchUser).toBe('function')
  })

  it('has doLogout method', async () => {
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
    await wrapper.vm.$nextTick()
    expect(typeof wrapper.vm.doLogout).toBe('function')
  })
})
