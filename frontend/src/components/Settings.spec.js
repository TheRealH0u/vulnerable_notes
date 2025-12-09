import { describe, it, expect, vi, beforeEach } from 'vitest'
import { mount } from '@vue/test-utils'
import Settings from '../components/Settings.vue'

vi.mock('axios', () => ({
  default: {
    get: vi.fn(),
    post: vi.fn()
  }
}))

describe('Settings Component', () => {
  let wrapper

  beforeEach(() => {
    wrapper = mount(Settings, {
      global: {
        mocks: {
          $router: {
            push: vi.fn()
          }
        }
      }
    })
  })

  it('renders settings form', () => {
    expect(wrapper.find('h3').text()).toBe('Settings')
  })

  it('has username field (readonly)', () => {
    const inputs = wrapper.findAll('input')
    expect(inputs.length).toBeGreaterThanOrEqual(1)
  })

  it('has email field (readonly)', () => {
    const inputs = wrapper.findAll('input')
    expect(inputs.length).toBeGreaterThanOrEqual(2)
  })

  it('has password input field', () => {
    const passwordInput = wrapper.find('input[type="password"]')
    expect(passwordInput.exists()).toBe(true)
  })

  it('has update password button', () => {
    const button = wrapper.find('button[type="submit"]')
    expect(button.text()).toBe('Update password')
  })

  it('initializes with empty password', () => {
    expect(wrapper.vm.password).toBe('')
  })

  it('has update method', () => {
    expect(typeof wrapper.vm.update).toBe('function')
  })

  it('updates password field on input', async () => {
    const passwordInput = wrapper.find('input[type="password"]')
    await passwordInput.setValue('newpass123')
    expect(wrapper.vm.password).toBe('newpass123')
  })

  it('initializes username and email as empty', () => {
    expect(wrapper.vm.username).toBe('')
    expect(wrapper.vm.email).toBe('')
  })

  it('sets readonly attribute on username field', () => {
    const inputs = wrapper.findAll('input')
    expect(inputs[0].attributes('readonly')).toBeDefined()
  })
})
