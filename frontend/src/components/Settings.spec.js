import { describe, it, expect, vi } from 'vitest'
import { mount } from '@vue/test-utils'
import Settings from './Settings.vue'
import axios from 'axios'

// Mock axios
vi.mock('axios', () => ({
  default: {
    get: vi.fn(() => Promise.resolve({ data: { username: 'testuser', email: 'test@example.com' } })),
    post: vi.fn(() => Promise.resolve({ data: { message: 'updated' } }))
  }
}))

describe('Settings Component', () => {
  it('renders settings form', () => {
    const wrapper = mount(Settings, {
      global: {
        mocks: {
          $router: { push: vi.fn() }
        }
      }
    })
    expect(wrapper.find('h3').text()).toBe('Settings')
  })

  it('has username field (readonly)', () => {
    const wrapper = mount(Settings, {
      global: {
        mocks: { $router: { push: vi.fn() } }
      }
    })
    const inputs = wrapper.findAll('input')
    expect(inputs.length).toBeGreaterThanOrEqual(1)
  })

  it('has email field (readonly)', () => {
    const wrapper = mount(Settings, {
      global: {
        mocks: { $router: { push: vi.fn() } }
      }
    })
    const inputs = wrapper.findAll('input')
    expect(inputs.length).toBeGreaterThanOrEqual(2)
  })

  it('has password input field', () => {
    const wrapper = mount(Settings, {
      global: {
        mocks: { $router: { push: vi.fn() } }
      }
    })
    const passwordInput = wrapper.find('input[type="password"]')
    expect(passwordInput.exists()).toBe(true)
  })

  it('has update password button', () => {
    const wrapper = mount(Settings, {
      global: {
        mocks: { $router: { push: vi.fn() } }
      }
    })
    const button = wrapper.find('button[type="submit"]')
    expect(button.text()).toBe('Update password')
  })

  it('initializes with empty password', () => {
    const wrapper = mount(Settings, {
      global: {
        mocks: { $router: { push: vi.fn() } }
      }
    })
    expect(wrapper.vm.password).toBe('')
  })

  it('has update method', () => {
    const wrapper = mount(Settings, {
      global: {
        mocks: { $router: { push: vi.fn() } }
      }
    })
    expect(typeof wrapper.vm.update).toBe('function')
  })

  it('updates password field on input', async () => {
    const wrapper = mount(Settings, {
      global: {
        mocks: { $router: { push: vi.fn() } }
      }
    })
    const passwordInput = wrapper.find('input[type="password"]')
    await passwordInput.setValue('newpass123')
    expect(wrapper.vm.password).toBe('newpass123')
  })

  it('initializes username and email as empty', () => {
    const wrapper = mount(Settings, {
      global: {
        mocks: { $router: { push: vi.fn() } }
      }
    })
    expect(wrapper.vm.username).toBe('')
    expect(wrapper.vm.email).toBe('')
  })
})
