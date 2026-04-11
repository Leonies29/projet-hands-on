let rows = ['Ligne exemple 1', 'Ligne exemple 2']

function wait(ms = 280) {
  return new Promise((resolve) => setTimeout(resolve, ms))
}

export async function mockGetData() {
  await wait()
  return { rows: [...rows] }
}

export async function mockPostData(body) {
  await wait()
  const line = body?.line
  if (typeof line !== 'string' || !line.trim()) {
    throw new Error('Le corps doit contenir une chaîne "line" non vide.')
  }
  rows = [...rows, line.trim()]
  return { ok: true }
}

export async function mockGetPoem() {
  await wait(400)
  return {
    poem:
      'Sous le ciel de démonstration,\n' +
      'Le frontend trace sa route seul.\n' +
      'Quand l’API rejoindra la mission,\n' +
      'Il suffira de couper le mock.',
  }
}
