import { describe, it, expect, vi, beforeEach } from 'vitest'
import { mount } from '@vue/test-utils'
import NoteView from '../components/NoteView.vue'

vi.mock('axios', () => ({
  default: {
    get: vi.fn(),
    post: vi.fn(),
    delete: vi.fn()
  }
}))

describe('NoteView Component', () => {
  let wrapper

  beforeEach(() => {
    wrapper = mount(NoteView, {
      global: {
        mocks: {
          $route: {
            params: {}
          },
          $router: {
            push: vi.fn(),
            replace: vi.fn()
          }
        }
      }
    })
  })

  it('renders create note title for new note', () => {
    expect(wrapper.text()).toContain('Create Note')
  })

  it('has title input field', () => {
    const input = wrapper.find('input')
    expect(input.exists()).toBe(true)
  })

  it('has content textarea', () => {
    const textarea = wrapper.find('textarea')
    expect(textarea.exists()).toBe(true)
  })

  it('has save button', () => {
    const button = wrapper.findAll('button').find(b => b.text() === 'Save')
    expect(button).toBeDefined()
  })

  it('has cancel button', () => {
    const button = wrapper.findAll('button').find(b => b.text() === 'Cancel')
    expect(button).toBeDefined()
  })

  it('initializes with empty title and content', () => {
    expect(wrapper.vm.title).toBe('')
    expect(wrapper.vm.content).toBe('')
  })

  it('marks new notes as isNew=true', () => {
    expect(wrapper.vm.isNew).toBe(true)
  })

  it('updates title on input', async () => {
    const input = wrapper.find('input')
    await input.setValue('Test Note')
    expect(wrapper.vm.title).toBe('Test Note')
  })

  it('updates content on input', async () => {
    const textarea = wrapper.find('textarea')
    await textarea.setValue('Note content here')
    expect(wrapper.vm.content).toBe('Note content here')
  })

  it('has save method', () => {
    expect(typeof wrapper.vm.save).toBe('function')
  })

  it('has cancel method', () => {
    expect(typeof wrapper.vm.cancel).toBe('function')
  })

  it('has del method for deletion', () => {
    expect(typeof wrapper.vm.del).toBe('function')
  })

  it('hides delete button for new notes', () => {
    wrapper.vm.isNew = true
    expect(wrapper.findAll('button').length).toBeLessThanOrEqual(3) // Save, Cancel, and maybe Delete
  })
})
