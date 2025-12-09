import { describe, it, expect, vi } from 'vitest'
import { mount } from '@vue/test-utils'
import NoteView from './NoteView.vue'

vi.mock('axios', () => ({
  default: {
    get: vi.fn(() => Promise.resolve({ data: { notes: [] } })),
    post: vi.fn(() => Promise.resolve({ data: { message: 'saved' } })),
    delete: vi.fn(() => Promise.resolve({ data: { message: 'deleted' } }))
  }
}))

describe('NoteView Component', () => {
  it('renders create note title for new note', () => {
    const wrapper = mount(NoteView, {
      global: {
        mocks: {
          $route: { params: {} },
          $router: { push: vi.fn(), replace: vi.fn() }
        }
      }
    })
    expect(wrapper.text()).toContain('Create Note')
  })

  it('has title input field', () => {
    const wrapper = mount(NoteView, {
      global: {
        mocks: {
          $route: { params: {} },
          $router: { push: vi.fn(), replace: vi.fn() }
        }
      }
    })
    const input = wrapper.find('input')
    expect(input.exists()).toBe(true)
  })

  it('has content textarea', () => {
    const wrapper = mount(NoteView, {
      global: {
        mocks: {
          $route: { params: {} },
          $router: { push: vi.fn(), replace: vi.fn() }
        }
      }
    })
    const textarea = wrapper.find('textarea')
    expect(textarea.exists()).toBe(true)
  })

  it('has save button', () => {
    const wrapper = mount(NoteView, {
      global: {
        mocks: {
          $route: { params: {} },
          $router: { push: vi.fn(), replace: vi.fn() }
        }
      }
    })
    const buttons = wrapper.findAll('button')
    const saveButton = buttons.find(b => b.text() === 'Save')
    expect(saveButton).toBeDefined()
  })

  it('has cancel button', () => {
    const wrapper = mount(NoteView, {
      global: {
        mocks: {
          $route: { params: {} },
          $router: { push: vi.fn(), replace: vi.fn() }
        }
      }
    })
    const buttons = wrapper.findAll('button')
    const cancelButton = buttons.find(b => b.text() === 'Cancel')
    expect(cancelButton).toBeDefined()
  })

  it('initializes with empty title and content', () => {
    const wrapper = mount(NoteView, {
      global: {
        mocks: {
          $route: { params: {} },
          $router: { push: vi.fn(), replace: vi.fn() }
        }
      }
    })
    expect(wrapper.vm.title).toBe('')
    expect(wrapper.vm.content).toBe('')
  })

  it('marks new notes as isNew=true', () => {
    const wrapper = mount(NoteView, {
      global: {
        mocks: {
          $route: { params: {} },
          $router: { push: vi.fn(), replace: vi.fn() }
        }
      }
    })
    expect(wrapper.vm.isNew).toBe(true)
  })

  it('updates title on input', async () => {
    const wrapper = mount(NoteView, {
      global: {
        mocks: {
          $route: { params: {} },
          $router: { push: vi.fn(), replace: vi.fn() }
        }
      }
    })
    const input = wrapper.find('input')
    await input.setValue('Test Note')
    expect(wrapper.vm.title).toBe('Test Note')
  })

  it('updates content on input', async () => {
    const wrapper = mount(NoteView, {
      global: {
        mocks: {
          $route: { params: {} },
          $router: { push: vi.fn(), replace: vi.fn() }
        }
      }
    })
    const textarea = wrapper.find('textarea')
    await textarea.setValue('Note content here')
    expect(wrapper.vm.content).toBe('Note content here')
  })

  it('has save method', () => {
    const wrapper = mount(NoteView, {
      global: {
        mocks: {
          $route: { params: {} },
          $router: { push: vi.fn(), replace: vi.fn() }
        }
      }
    })
    expect(typeof wrapper.vm.save).toBe('function')
  })

  it('has cancel method', () => {
    const wrapper = mount(NoteView, {
      global: {
        mocks: {
          $route: { params: {} },
          $router: { push: vi.fn(), replace: vi.fn() }
        }
      }
    })
    expect(typeof wrapper.vm.cancel).toBe('function')
  })

  it('has del method for deletion', () => {
    const wrapper = mount(NoteView, {
      global: {
        mocks: {
          $route: { params: {} },
          $router: { push: vi.fn(), replace: vi.fn() }
        }
      }
    })
    expect(typeof wrapper.vm.del).toBe('function')
  })
})
