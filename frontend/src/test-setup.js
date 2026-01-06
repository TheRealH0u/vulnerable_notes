import { vi } from 'vitest'

// Mock axios globally for all tests
vi.mock('axios', () => {
  const mockAxiosInstance = {
    get: vi.fn(() => Promise.resolve({ data: {} })),
    post: vi.fn(() => Promise.resolve({ data: {} })),
    put: vi.fn(() => Promise.resolve({ data: {} })),
    delete: vi.fn(() => Promise.resolve({ data: {} })),
    interceptors: {
      request: { use: vi.fn((cb) => cb) },
      response: { use: vi.fn((cb) => cb) }
    }
  }
  
  return {
    default: {
      create: vi.fn(() => mockAxiosInstance),
      get: vi.fn(() => Promise.resolve({ data: {} })),
      post: vi.fn(() => Promise.resolve({ data: {} })),
      put: vi.fn(() => Promise.resolve({ data: {} })),
      delete: vi.fn(() => Promise.resolve({ data: {} }))
    }
  }
})
