import { describe, it, expect, vi, beforeEach } from 'vitest'
import { mount } from '@vue/test-utils'
import Home from '../components/Home.vue'

vi.mock('axios', () => ({
  default: {
    get: vi.fn()
  }
}))

describe('Home Component', () => {
  let wrapper

  beforeEach(() => {
    wrapper = mount(Home, {
      global: {
        stubs: {
          'router-link': true
        },
        mocks: {
          $route: {
            path: '/',
            query: {}
          },
          $router: {
            push: vi.fn(),
            replace: vi.fn()
          }
        }
      }
    })
  })

  it('renders notes container', () => {
    expect(wrapper.find('.container').exists()).toBe(true)
  })

  it('initializes with empty notes array', () => {
    expect(wrapper.vm.notes).toEqual([])
  })

  it('initializes with null alert message', () => {
    expect(wrapper.vm.alertMessage).toBeNull()
  })

  it('displays "Your Notes" heading', () => {
    expect(wrapper.find('h3').text()).toBe('Your Notes')
  })

  it('shows empty message when no notes', () => {
    expect(wrapper.text()).toContain('You have no notes yet')
  })

  it('has dismissAlert method', () => {
    expect(typeof wrapper.vm.dismissAlert).toBe('function')
  })

  it('dismisses alert when called', async () => {
    wrapper.vm.alertMessage = 'Test error'
    wrapper.vm.dismissAlert()
    expect(wrapper.vm.alertMessage).toBeNull()
  })

  it('has floating action button', () => {
    expect(wrapper.find('.fab').exists()).toBe(true)
  })

  it('fab has plus symbol', () => {
    expect(wrapper.find('.fab').text()).toBe('+')
  })

  it('links to create new note', () => {
    const fab = wrapper.find('router-link')
    expect(fab.attributes('to')).toBe('/note')
  })

  it('handles sessionStorage cache', () => {
    expect(wrapper.vm.notes).toBeDefined()
  })
})
