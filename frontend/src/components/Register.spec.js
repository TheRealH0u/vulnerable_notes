import { describe, it, expect, vi, beforeEach } from 'vitest'
import { mount } from '@vue/test-utils'
import Register from '../components/Register.vue'

vi.mock('axios', () => ({
  default: {
    post: vi.fn()
  }
}))

describe('Register Component', () => {
  let wrapper

  beforeEach(() => {
    wrapper = mount(Register, {
      global: {
        mocks: {
          $router: {
            push: vi.fn()
          }
        }
      }
    })
  })

  it('renders register form', () => {
    expect(wrapper.find('h2').text()).toBe('Register')
  })

  it('has username, email, password, and verify inputs', () => {
    const inputs = wrapper.findAll('input')
    expect(inputs.length).toBeGreaterThanOrEqual(4)
  })

  it('has register button', () => {
    const button = wrapper.find('button[type="submit"]')
    expect(button.text()).toBe('Register')
  })

  it('initializes with empty fields', () => {
    expect(wrapper.vm.username).toBe('')
    expect(wrapper.vm.email).toBe('')
    expect(wrapper.vm.password).toBe('')
    expect(wrapper.vm.verify).toBe('')
  })

  it('updates username on input', async () => {
    const input = wrapper.findAll('input')[0]
    await input.setValue('newuser')
    expect(wrapper.vm.username).toBe('newuser')
  })

  it('updates email on input', async () => {
    const input = wrapper.findAll('input')[1]
    await input.setValue('test@example.com')
    expect(wrapper.vm.email).toBe('test@example.com')
  })

  it('updates password on input', async () => {
    const input = wrapper.findAll('input[type="password"]')[0]
    await input.setValue('pass123')
    expect(wrapper.vm.password).toBe('pass123')
  })

  it('updates verify on input', async () => {
    const input = wrapper.findAll('input[type="password"]')[1]
    await input.setValue('pass123')
    expect(wrapper.vm.verify).toBe('pass123')
  })

  it('has doRegister method', () => {
    expect(typeof wrapper.vm.doRegister).toBe('function')
  })
})
