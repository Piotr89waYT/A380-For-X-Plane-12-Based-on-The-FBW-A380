import settings from 'renderer/rendererSettings';

export enum Simulators {
  Msfs2020 = 'msfs2020',
  Msfs2024 = 'msfs2024',
  XPlane12 = 'xplane12',
  XPlane11 = 'xplane11',
}

export const isXPlane = (sim: string): boolean => sim === Simulators.XPlane12 || sim === Simulators.XPlane11;

export const xplaneSimArgs = (sim: string): string[] => (sim === Simulators.XPlane11 ? ['--sim', 'xp11'] : []);

export type TypeOfSimulator = `${Simulators}` | Simulators;

export const enabledSimulators = () => {
  return Object.values(Simulators).filter(
    (sim) => (settings.get('mainSettings.simulator') as Record<Simulators, { enabled: boolean }>)[sim]?.enabled,
  );
};

export const nextSim = (sim: Simulators) => {
  const values = Object.values(enabledSimulators());
  const currentIndex = values.indexOf(sim);
  const nextIndex = (currentIndex + 1) % values.length;
  return values[nextIndex];
};

export const managedSim = () => {
  return settings.get('cache.main.managedSim') as Simulators;
};

export const setManagedSim = (sim: Simulators) => {
  settings.set('cache.main.managedSim', sim);
};
