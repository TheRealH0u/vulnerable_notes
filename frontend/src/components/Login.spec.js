import { describe, it, expect, vi, beforeEach } from 'vitest'
import { mount } from '@vue/test-utils'
import Login from '../components/Login.vue'

// Mock axios
vi.mock('axios', () => ({
  default: {
    post: vi.fn(),
    get: vi.fn()
  }
}))

describe('Login Component', () => {
  let wrapper

  beforeEach(() => {
    wrapper = mount(Login, {
      global: {
        mocks: {
          $router: {
            push: vi.fn()
          }
        }
      }
    })
  })

  it('renders login form', () => {
    expect(wrapper.find('h2').text()).toBe('Login')
  })

  it('has username input field', () => {
    const inputs = wrapper.findAll('input')
    expect(inputs.length).toBeGreaterThanOrEqual(1)
  })

  it('has password input field', () => {
    const passwordInputs = wrapper.findAll('input[type="password"]')
    expect(passwordInputs.length).toBeGreaterThanOrEqual(1)
  })

  it('has login button', () => {
    const button = wrapper.find('button[type="submit"]')
    expect(button.text()).toBe('Login')
  })

  it('has register link', () => {
    const link = wrapper.find('router-link')
    expect(link.attributes('to')).toBe('/register')
  })

  it('initializes with empty username and password', () => {
    expect(wrapper.vm.username).toBe('')
    expect(wrapper.vm.password).toBe('')
  })

  it('updates username when input changes', async () => {
    const input = wrapper.findAll('input')[0]
    await input.setValue('testuser')
    expect(wrapper.vm.username).toBe('testuser')
  })

  it('updates password when input changes', async () => {
    const passwordInput = wrapper.find('input[type="password"]')
    await passwordInput.setValue('password123')
    expect(wrapper.vm.password).toBe('password123')
  })

  it('has doLogin method', () => {
    expect(typeof wrapper.vm.doLogin).toBe('function')
  })

  it('displays card layout', () => {
    expect(wrapper.find('.card').exists()).toBe(true)
  })

  it('has proper bootstrap classes', () => {
    const container = wrapper.find('.container')
    expect(container.exists()).toBe(true)
  })
})
