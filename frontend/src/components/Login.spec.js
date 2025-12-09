import { describe, it, expect, vi } from 'vitest'
import { mount } from '@vue/test-utils'
import Login from './Login.vue'

// Mock axios
vi.mock('axios', () => ({
  default: {
    post: vi.fn(() => Promise.resolve({ data: { message: 'ok' } })),
    get: vi.fn(() => Promise.resolve({ data: { notes: [] } }))
  }
}))

describe('Login Component', () => {
  it('renders login form', () => {
    const wrapper = mount(Login, {
      global: {
        stubs: {
          'router-link': true
        },
        mocks: {
          $router: { push: vi.fn() }
        }
      }
    })
    expect(wrapper.find('h2').text()).toBe('Login')
  })

  it('has username input field', () => {
    const wrapper = mount(Login, {
      global: {
        stubs: { 'router-link': true },
        mocks: { $router: { push: vi.fn() } }
      }
    })
    const inputs = wrapper.findAll('input')
    expect(inputs.length).toBeGreaterThanOrEqual(1)
  })

  it('has password input field', () => {
    const wrapper = mount(Login, {
      global: {
        stubs: { 'router-link': true },
        mocks: { $router: { push: vi.fn() } }
      }
    })
    const passwordInputs = wrapper.findAll('input[type="password"]')
    expect(passwordInputs.length).toBeGreaterThanOrEqual(1)
  })

  it('has login button', () => {
    const wrapper = mount(Login, {
      global: {
        stubs: { 'router-link': true },
        mocks: { $router: { push: vi.fn() } }
      }
    })
    const button = wrapper.find('button[type="submit"]')
    expect(button.text()).toBe('Login')
  })

  it('has register link', () => {
    const wrapper = mount(Login, {
      global: {
        stubs: { 'router-link': { template: '<div><slot /></div>' } },
        mocks: { $router: { push: vi.fn() } }
      }
    })
    expect(wrapper.html()).toContain('Register')
  })

  it('initializes with empty username and password', () => {
    const wrapper = mount(Login, {
      global: {
        stubs: { 'router-link': true },
        mocks: { $router: { push: vi.fn() } }
      }
    })
    expect(wrapper.vm.username).toBe('')
    expect(wrapper.vm.password).toBe('')
  })

  it('updates username when input changes', async () => {
    const wrapper = mount(Login, {
      global: {
        stubs: { 'router-link': true },
        mocks: { $router: { push: vi.fn() } }
      }
    })
    const inputs = wrapper.findAll('input')
    await inputs[0].setValue('testuser')
    expect(wrapper.vm.username).toBe('testuser')
  })

  it('updates password when input changes', async () => {
    const wrapper = mount(Login, {
      global: {
        stubs: { 'router-link': true },
        mocks: { $router: { push: vi.fn() } }
      }
    })
    const passwordInput = wrapper.find('input[type="password"]')
    await passwordInput.setValue('password123')
    expect(wrapper.vm.password).toBe('password123')
  })

  it('has doLogin method', () => {
    const wrapper = mount(Login, {
      global: {
        stubs: { 'router-link': true },
        mocks: { $router: { push: vi.fn() } }
      }
    })
    expect(typeof wrapper.vm.doLogin).toBe('function')
  })
})
