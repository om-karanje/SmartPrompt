export default function ConstraintList({ constraints = [] }) {
  return (
    <section className="panel">
      <h3>Detected Constraints</h3>
      {constraints.length === 0 ? (
        <p>No explicit constraints detected.</p>
      ) : (
        <ul className="list">
          {constraints.map((constraint, index) => (
            <li key={`${constraint.label}-${index}`}>
              <span className="badge success">✓</span> {constraint.label}
              <div>{constraint.detail}</div>
            </li>
          ))}
        </ul>
      )}
    </section>
  );
}
