/**
 * generates a 2d matrix of X x Y neurons                      (e.g. 25 x 25 = 625 total neurons)
 * defines an activation pool of random length                 (e.g. 3 neurons to be activated)
 * randomly assigns specific neurons to this pool              (e.g. n1, n14, n99)
 * activates each with a random activity level between 0 and 1 (e.g. 0.28)
 */
export const randActivity = (
  opts: {
    neuronsX: number;
    neuronsY: number;
  } = { neuronsX: 25, neuronsY: 25 }
) => {
  const totalNeurons = opts.neuronsX * opts.neuronsY;
  const neuronsToActivate = Math.floor(Math.random() * (100 - 1) + 1);

  const getRandomNeuron = () =>
    Math.floor(Math.random() * (totalNeurons - 1) + 1);

  const activatedNeuronIds = Array.from(Array(neuronsToActivate)).map(
    getRandomNeuron
  );

  return Array.from(Array(opts.neuronsX)).map((_, xI: number) => {
    return Array.from(Array(opts.neuronsY)).map((_, yI: number) => {
      const neuronId = (xI + 1) * (yI + 1);
      return activatedNeuronIds.includes(neuronId) ? Math.random() : 0;
    });
  });
};
