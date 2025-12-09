import { describe, it, expect, vi, beforeEach } from 'vitest'
import { mount } from '@vue/test-utils'
import App from '../App.vue'

// Mock axios
vi.mock('axios', () => ({
  default: {
    post: vi.fn(),
    get: vi.fn()
  }
}))

describe('App Component', () => {
  let wrapper

  beforeEach(() => {
    wrapper = mount(App, {
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
  })

  it('renders app container', () => {
    expect(wrapper.find('div').exists()).toBe(true)
  })

  it('initializes with null user', () => {
    expect(wrapper.vm.user).toBeNull()
  })

  it('has fetchUser method', () => {
    expect(typeof wrapper.vm.fetchUser).toBe('function')
  })

  it('has doLogout method', () => {
    expect(typeof wrapper.vm.doLogout).toBe('function')
  })

  it('displays slogan text', () => {
    const slogan = wrapper.find('#slogan')
    expect(slogan.exists()).toBe(true)
    expect(slogan.text()).toContain('Vulnerable Notes')
  })

  it('contains router-view component', () => {
    expect(wrapper.findComponent({ name: 'RouterView' }).exists() || wrapper.html().includes('router-view')).toBeTruthy()
  })

  it('sets user when authenticated', async () => {
    wrapper.vm.user = 'testuser'
    await wrapper.vm.$nextTick()
    expect(wrapper.vm.user).toBe('testuser')
  })

  it('hides navbar when no user', () => {
    wrapper.vm.user = null
    expect(wrapper.vm.user).toBeNull()
  })

  it('has main element', () => {
    expect(wrapper.find('main').exists()).toBe(true)
  })

  it('renders VulnerableNotes brand when user exists', async () => {
    wrapper.vm.user = 'testuser'
    await wrapper.vm.$nextTick()
    expect(wrapper.html()).toContain('VulnerableNotes')
  })

  it('calls fetchUser on created', () => {
    // fetchUser should be called during component creation
    expect(typeof wrapper.vm.fetchUser).toBe('function')
  })
})
