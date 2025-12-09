import { describe, it, expect, vi } from 'vitest'
import { mount } from '@vue/test-utils'
import Home from './Home.vue'

vi.mock('axios', () => ({
  default: {
    get: vi.fn(() => Promise.resolve({ data: { notes: [] } }))
  }
}))

describe('Home Component', () => {
  it('renders notes container', () => {
    const wrapper = mount(Home, {
      global: {
        stubs: { 'router-link': true },
        mocks: {
          $route: { path: '/', query: {} },
          $router: { push: vi.fn(), replace: vi.fn() }
        }
      }
    })
    expect(wrapper.find('.container').exists()).toBe(true)
  })

  it('initializes with empty notes array', () => {
    const wrapper = mount(Home, {
      global: {
        stubs: { 'router-link': true },
        mocks: {
          $route: { path: '/', query: {} },
          $router: { push: vi.fn(), replace: vi.fn() }
        }
      }
    })
    expect(wrapper.vm.notes).toEqual([])
  })

  it('initializes with null alert message', () => {
    const wrapper = mount(Home, {
      global: {
        stubs: { 'router-link': true },
        mocks: {
          $route: { path: '/', query: {} },
          $router: { push: vi.fn(), replace: vi.fn() }
        }
      }
    })
    expect(wrapper.vm.alertMessage).toBeNull()
  })

  it('displays "Your Notes" heading', () => {
    const wrapper = mount(Home, {
      global: {
        stubs: { 'router-link': true },
        mocks: {
          $route: { path: '/', query: {} },
          $router: { push: vi.fn(), replace: vi.fn() }
        }
      }
    })
    expect(wrapper.find('h3').text()).toBe('Your Notes')
  })

  it('shows empty message when no notes', () => {
    const wrapper = mount(Home, {
      global: {
        stubs: { 'router-link': true },
        mocks: {
          $route: { path: '/', query: {} },
          $router: { push: vi.fn(), replace: vi.fn() }
        }
      }
    })
    expect(wrapper.text()).toContain('You have no notes yet')
  })

  it('has dismissAlert method', () => {
    const wrapper = mount(Home, {
      global: {
        stubs: { 'router-link': true },
        mocks: {
          $route: { path: '/', query: {} },
          $router: { push: vi.fn(), replace: vi.fn() }
        }
      }
    })
    expect(typeof wrapper.vm.dismissAlert).toBe('function')
  })

  it('dismisses alert when called', async () => {
    const wrapper = mount(Home, {
      global: {
        stubs: { 'router-link': true },
        mocks: {
          $route: { path: '/', query: {} },
          $router: { push: vi.fn(), replace: vi.fn() }
        }
      }
    })
    wrapper.vm.alertMessage = 'Test error'
    wrapper.vm.dismissAlert()
    expect(wrapper.vm.alertMessage).toBeNull()
  })

  it('has floating action button', () => {
    const wrapper = mount(Home, {
      global: {
        stubs: { 'router-link': true },
        mocks: {
          $route: { path: '/', query: {} },
          $router: { push: vi.fn(), replace: vi.fn() }
        }
      }
    })
    expect(wrapper.find('.fab').exists()).toBe(true)
  })
})
